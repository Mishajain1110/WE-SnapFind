import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models
import torch.nn.functional as F
import os

# Load MobileNetV3-Large model
model = models.mobilenet_v3_large(pretrained=True)
model = torch.nn.Sequential(*list(model.children())[:-1])  # Remove classification head
model.eval()

# Adaptive pooling to get a fixed-size feature vector
adaptive_pool = torch.nn.AdaptiveAvgPool2d((1, 1))

def preprocess_image(image_path):
    """Preprocess image with data augmentation."""
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.RandomRotation(degrees=10),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(image_path).convert("RGB")
    return transform(image).unsqueeze(0)

def extract_features(image_path):
    """Extract deep features from MobileNetV3-Large."""
    image = preprocess_image(image_path)
    with torch.no_grad():
        features = model(image)  # Extract feature maps
        features = adaptive_pool(features)  # Reduce dimensionality
        features = features.squeeze().flatten()  # Flatten to 1D vector
    return features

def compare_images(img1_path, img2_path):
    """Compute similarity using cosine similarity & Euclidean distance."""
    features1 = extract_features(img1_path)
    features2 = extract_features(img2_path)

    # Normalize feature vectors (L2 normalization)
    features1 = F.normalize(features1, p=2, dim=0)
    features2 = F.normalize(features2, p=2, dim=0)

    # Compute Cosine Similarity (higher = more similar)
    cosine_sim = torch.nn.functional.cosine_similarity(features1.unsqueeze(0), features2.unsqueeze(0)).item()

    # Compute Euclidean Distance (lower = more similar)
    euclidean_dist = torch.dist(features1, features2, p=2).item()

    # Weighted Similarity Score (higher = more similar)
    similarity_score = (cosine_sim * 0.7) - (euclidean_dist * 0.3)

    return similarity_score

def find_best_matching_images(input_image_path, image_dir):
    """Find the most similar images to the input image in a directory."""
    if not os.path.exists(image_dir):
        print(f"Error: Directory '{image_dir}' does not exist.")
        return []

    best_matching_images = []
    best_similarity_score = float('-inf') 

    for image_file in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_file)

        if image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            similarity_score = compare_images(image_path, input_image_path)
            print(f"Similarity Score ({image_file}): {similarity_score}")

            if similarity_score >= best_similarity_score:
                best_matching_images.append((image_path, similarity_score))
                best_similarity_score = similarity_score

    best_matching_images.sort(key=lambda x: x[1], reverse=True)

    return best_matching_images[:5] 

image_dir = "lost-and-found/media/posts"
input_image_path = "lost-and-found/media/posts/bottle.jpeg"

best_matches = find_best_matching_images(input_image_path, image_dir)

print("\nTop Matching Images:")
for match in best_matches:
    print(f"Image: {match[0]}, Similarity Score: {match[1]:.4f}")
