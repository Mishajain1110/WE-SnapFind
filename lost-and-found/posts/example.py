import spacy

# Load the pre-trained model
nlp = spacy.load('en_core_web_md')

# Example sentences
text1 = "I lost my wallet in the park."
text2 = "Someone found a wallet in the park."

# Compute similarity
doc1 = nlp(text1)
doc2 = nlp(text2)
similarity = doc1.similarity(doc2)
print(f"Similarity: {similarity}")