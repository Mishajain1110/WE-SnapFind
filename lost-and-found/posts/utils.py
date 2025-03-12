# posts/utils.py
import spacy
from .models import PostPicture
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision import models
import numpy as np
import os
import faiss
import sqlite3
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from sklearn.preprocessing import MinMaxScaler

nlp = spacy.load('en_core_web_md')

def compute_similarity(text1, text2):
    """
    Compute the cosine similarity between two texts using spaCy.
    """
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    similarity = doc1.similarity(doc2)
    return similarity

# BLIP model (for captioning)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image_path):
    print("Generating Caption..")
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    with torch.no_grad():
        caption_ids = blip_model.generate(**inputs)
    caption = processor.decode(caption_ids[0], skip_special_tokens=True)
    print("Caption Generated for ",image_path, caption)
    return caption

# MobileNetV3 model (for feature extraction)
mobilenet_model = models.mobilenet_v3_large(weights=models.MobileNet_V3_Large_Weights.DEFAULT)
mobilenet_model = torch.nn.Sequential(*list(mobilenet_model.children())[:-1]) 
mobilenet_model.eval()
torch.set_num_threads(1)  

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def preprocess_image(image_path):
    """Load and preprocess an image"""
    image = Image.open(image_path).convert("RGB")
    return transform(image).unsqueeze(0)

def extract_features(image_path):
    """Extract feature embeddings from MobileNetV3"""
    image = preprocess_image(image_path)
    with torch.no_grad():
        features = mobilenet_model(image).squeeze().flatten().numpy()  
    return features.astype('float32')

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image_features.db")

def create_database():
    """Create table for storing image features"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS image_features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_name TEXT UNIQUE,
                feature_vector BLOB
            )
        """)
        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Database Error: {e}")  

def build_feature_database(directory):
    """Extract and store feature vectors of all images"""
    create_database()
    
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return []  

    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"Found {len(image_files)} images in {directory}")
    
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda img: (img, extract_features(os.path.join(directory, img))), image_files))

    for img_name, features in results:
        store_feature_in_db(img_name, features)

    print(f"Database built with {len(image_files)} images.")

def store_feature_in_db(image_name, features):
    """Insert image features into sqlite"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    feature_bytes = features.tobytes()
    cur.execute("INSERT OR REPLACE INTO image_features (image_name, feature_vector) VALUES (?, ?)", 
            (image_name, feature_bytes))
    conn.commit()
    cur.close()
    conn.close()

def load_features_from_db():
    """Load all stored image features for FAISS indexing"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT image_name, feature_vector FROM image_features")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print(f"Retrieved {len(rows)} images from DB")
    
    image_names = []
    feature_vectors = []

    for row in rows:
        image_name, feature_bytes = row
        features = np.frombuffer(feature_bytes, dtype=np.float32)  
        image_names.append(image_name)
        feature_vectors.append(features)

    if len(feature_vectors) == 0:
        return None, []

    return np.array(feature_vectors, dtype=np.float32), image_names

def load_faiss_index():
    """Load FAISS index from database"""
    feature_matrix, image_names = load_features_from_db()

    if feature_matrix is None:
        return None, []

    index = faiss.IndexFlatL2(feature_matrix.shape[1])
    index.add(feature_matrix)

    return index, image_names

def find_similar_images(input_image_path, faiss_index, image_names):
    """Find most similar images using FAISS"""
    if faiss_index is None:
        print("No images found in the database.")
        return []

    query_features = extract_features(input_image_path).reshape(1, -1)
    distances, indices = faiss_index.search(query_features, len(image_names))

    return [(image_names[idx], distances[0][i]) for i, idx in enumerate(indices[0])]

def normalize_distances(distances):
    """Normalize FAISS distances to similarity scores (higher is better)."""
    if len(distances) == 0:
        return []
    
    scaler = MinMaxScaler(feature_range=(0, 1))  
    distances = np.array(distances).reshape(-1, 1)
    similarities = 1 - scaler.fit_transform(distances)  
    return similarities.flatten()

def find_similar_lost_posts(new_post, lost_posts, text_weight=0.5, image_weight=0.5, threshold=0.7):
    """
    Find lost posts that are similar to the new found post.
    """
    similar_posts = []

    post_picture = PostPicture.objects.filter(post=new_post).first()

    if not new_post.desc or new_post.desc.strip() == "":
        if post_picture and post_picture.picture: 
            new_post.desc = generate_caption(post_picture.picture.path)

    new_text = f"{new_post.title} : {new_post.desc}"
    print(f"Updated new_post.desc => {new_post.desc}")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_DIR = os.path.join(BASE_DIR, 'media', 'posts')

    image_dir = MEDIA_DIR
    input_image_path = post_picture.picture.path if post_picture and post_picture.picture else None
    image_results = []

    build_feature_database(image_dir)

    faiss_index, image_names = load_faiss_index()
    print(f"FAISS Index Loaded: {faiss_index is not None}, Image Names: {len(image_names)}")

    if input_image_path and faiss_index:
        image_results = find_similar_images(input_image_path, faiss_index, image_names)
        print("\n🔹 Top Matching Images:")
        for match in image_results:
            print(f"Image: {match[0]}, Distance: {match[1]:.4f}")

    image_names_list = [match[0] for match in image_results]
    faiss_distances = [match[1] for match in image_results]
    image_similarities = normalize_distances(faiss_distances)

    image_similarity_dict = {img: sim for img, sim in zip(image_names_list, image_similarities)}

    print(f"Number of lost posts: {len(lost_posts)}")

    for lost_post in lost_posts:
        lost_picture = PostPicture.objects.filter(post=lost_post).first()
        
        if not lost_post.desc or lost_post.desc.strip() == "":
            if lost_picture and lost_picture.picture:
                lost_post.desc = generate_caption(lost_picture.picture.path)

        lost_text = f"{lost_post.title} {lost_post.desc}"
        text_sim = compute_similarity(new_text, lost_text)

        image_sim = 0
        if lost_picture and lost_picture.picture:
            lost_image_name = os.path.basename(lost_picture.picture.path)
            image_sim = image_similarity_dict.get(lost_image_name, 0) 

        combined_similarity = (text_weight * text_sim) + (image_weight * image_sim)

        if combined_similarity > threshold:
            similar_posts.append((lost_post, combined_similarity))
        
        print(f"Lost Post: {lost_post.id} | Text Sim: {text_sim:.4f} | Image Sim: {image_sim:.4f} | Combined: {combined_similarity:.4f}")

    similar_posts = sorted(similar_posts, key=lambda x: x[1], reverse=True)

    return similar_posts