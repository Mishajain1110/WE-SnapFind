import spacy
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Load the pre-trained spaCy model
nlp = spacy.load("en_core_web_md")

# Load BLIP model and processor for image captioning
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def compute_similarity(text1, text2):
    """
    Compute the cosine similarity between two texts using spaCy.
    """
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    return doc1.similarity(doc2)

def generate_caption(image_path):
    """
    Generate an image caption using the BLIP model.
    """
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(image, return_tensors="pt")
        with torch.no_grad():
            caption_ids = model.generate(**inputs)
        print("Gnerating Caption for Image")
        return processor.decode(caption_ids[0], skip_special_tokens=True)
    except Exception as e:
        print(f"Error generating caption: {e}")
        return ""

def find_similar_lost_posts(new_post, lost_posts, threshold=0.7):
    """
    Find lost posts that are similar to the new found post.
    """
    if not lost_posts or not isinstance(lost_posts, list):
        return []

    # Ensure new_post.desc is available
    if not new_post.desc or new_post.desc.strip() == "":
        if hasattr(new_post, "image") and new_post.image:
            new_post.desc = generate_caption(new_post.image)
        else:
            new_post.desc = ""

    new_text = f"{new_post.title} {new_post.desc}".strip()

    similar_posts = []
    
    for lost_post in lost_posts:
        # Ensure lost_post.desc is available
        if not lost_post.desc or lost_post.desc.strip() == "":
            if hasattr(lost_post, "image") and lost_post.image:
                lost_post.desc = generate_caption(lost_post.image)
            else:
                lost_post.desc = ""

        lost_text = f"{lost_post.title} {lost_post.desc}".strip()

        if new_text and lost_text:
            similarity = compute_similarity(new_text, lost_text)
            if similarity > threshold:
                similar_posts.append((lost_post, similarity))

    # Sort by similarity in descending order
    similar_posts.sort(key=lambda x: x[1], reverse=True)

    return similar_posts
