# File : similarities.py

# Description: contains logic for measuring the similarity between summaries of 
#              lectures.

# Depends on: summarizer.py

# Date: December 2023

# Authors: Themistoklis Haris, Themistoklis Nikas

sumSimilarities = {}

vectorizer = CountVectorizer()

similarities = []
for lec1, lec2 in lectures:
    sum1 = lecture_dict[lec1]
    sum2 = lecture_dict[lec2]

    vectorized_texts = vectorizer.fit_transform([sum1, sum2])

    # Calculate the cosine similarity
    cosine_sim = cosine_similarity(vectorized_texts)
    
    print(f"Lectures: {lec1} and {lec2} have a similarity of: {cosine_sim[0, 1]:.3f}")
    similarities.append(cosine_sim[0, 1])

avgSim = statistics.mean(similarities)
print("-"*100)
print("Average cosine similarity:", avgSim)

output_folder = "Word Clouds"
os.makedirs(output_folder, exist_ok=True)
