# posts/utils.py
import spacy

# Load the pre-trained spaCy model
nlp = spacy.load('en_core_web_md')

def compute_similarity(text1, text2):
    """
    Compute the cosine similarity between two texts using spaCy.
    """
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    similarity = doc1.similarity(doc2)
    return similarity

def find_similar_lost_posts(new_post, lost_posts, threshold=0.7):
    """
    Find lost posts that are similar to the new found post.
    """
    similar_posts = []

    # Combine title and description for the new post
    new_text = f"{new_post.title} {new_post.desc}"

    for lost_post in lost_posts:
        # Combine title and description for the lost post
        lost_text = f"{lost_post.title} {lost_post.desc}"

        # Compute similarity
        similarity = compute_similarity(new_text, lost_text)

        # If similarity is above the threshold, add to similar posts
        if similarity > threshold:
            similar_posts.append((lost_post, similarity))

    # Sort similar posts by similarity score (descending)
    similar_posts.sort(key=lambda x: x[1], reverse=True)

    return similar_posts