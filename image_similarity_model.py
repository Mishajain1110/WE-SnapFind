import torch
import torchvision.transforms as transforms
from torchvision import models
import numpy as np
import os
import faiss
import mysql.connector
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

load_dotenv()

model = models.mobilenet_v3_large(weights=models.MobileNet_V3_Large_Weights.DEFAULT)
model = torch.nn.Sequential(*list(model.children())[:-1])  
model.eval()
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
        features = model(image).squeeze().flatten().numpy()  
    return features.astype('float32')

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}

def create_database():
    """Create table for storing image features"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS image_features (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image_name VARCHAR(255) UNIQUE,
            feature_vector LONGBLOB
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def build_feature_database(directory):
    """Extract and store feature vectors of all images"""
    create_database()

    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda img: (img, extract_features(os.path.join(directory, img))), image_files))

    for img_name, features in results:
        store_feature_in_db(img_name, features)

    print(f"Database built with {len(image_files)} images.")

def store_feature_in_db(image_name, features):
    """Insert image features into MySQL"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    feature_bytes = features.tobytes()
    cur.execute("INSERT INTO image_features (image_name, feature_vector) VALUES (%s, %s) ON DUPLICATE KEY UPDATE feature_vector = VALUES(feature_vector)",
                (image_name, feature_bytes))
    conn.commit()
    cur.close()
    conn.close()

def load_features_from_db():
    """Load all stored image features for FAISS indexing"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT image_name, feature_vector FROM image_features")
    rows = cur.fetchall()
    cur.close()
    conn.close()

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

def find_similar_images(input_image_path, faiss_index, image_names, top_k=5):
    """Find most similar images using FAISS"""
    if faiss_index is None:
        print("No images found in the database.")
        return []

    query_features = extract_features(input_image_path).reshape(1, -1)
    distances, indices = faiss_index.search(query_features, top_k)

    return [(image_names[idx], distances[0][i]) for i, idx in enumerate(indices[0])]

image_dir = "lost-and-found/media/posts"
input_image_path = "lost-and-found/media/posts/bottle.jpeg"

create_database()
build_feature_database(image_dir)

faiss_index, image_names = load_faiss_index()
best_matches = find_similar_images(input_image_path, faiss_index, image_names, top_k=10)

print("\nTop Matching Images:")
for match in best_matches:
    print(f"Image: {match[0]}, Distance: {match[1]:.4f}")
