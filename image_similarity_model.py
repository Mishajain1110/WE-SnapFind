import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models
import torch.nn.functional as F
import os

# Load MobileNetV3-Large model
model = models.mobilenet_v3_large(pretrained=True)
model.eval()

def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
    image = Image.open(image_path).convert("RGB")
    return transform(image).unsqueeze(0)

def extract_features(image_path):
    image = preprocess_image(image_path)
    with torch.no_grad():
        features = model(image).squeeze()
    return features

def compute_similarity(features1, features2):
    return F.cosine_similarity(features1.unsqueeze(0), features2.unsqueeze(0)).item()

def find_similar_images(input_image_path, directory):
    input_features = extract_features(input_image_path)
    similarity_scores = {}
    
    for image_file in os.listdir(directory):
        image_path = os.path.join(directory, image_file)
        if image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            features = extract_features(image_path)
            similarity = compute_similarity(input_features, features)
            similarity_scores[image_file] = similarity
            print(f"Similarity with {image_file}: {similarity:.4f}")
    
    return sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

image_dir = "lost-and-found/media/posts"
input_image_path = "lost-and-found/media/posts/bottle.jpeg"
best_matches = find_similar_images(input_image_path, image_dir)

print("\nTop Matching Images:")
for match in best_matches:
    print(f"Image: {match[0]}, Similarity Score: {match[1]:.4f}")
