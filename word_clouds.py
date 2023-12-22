# File : word_clouds.py

# Description: contains logic for creating word clouds from summaries of lecture
#              transcripts

# Depends on: summarizer.py

# Date: December 2023

# Authors: Themistoklis Nikas, Themistoklis Haris

custom_stopwords = set(STOPWORDS)
# Update stop words with the following that appear frequently in natural language
custom_stopwords.update(['going', 'know', 'okay', 'right', 'thing'])

# Create a single WordCloud instance outside the loop
wordcloud = WordCloud(width=800, height=400, background_color='black', max_words=100, collocations=True,
                      stopwords=custom_stopwords)

for title, summary in lecture_dict.items():
    if title in singles.keys():
        # Combine title and summary text
        text = f"{title} {summary}"

        # Generate word cloud for the current title and summary
        wordcloud.generate(text)
        
        fnameTitle = title.replace(" ", "_").replace("/", "_")
        output_path = os.path.join(output_folder, f"{fnameTitle}.png")
        
        wordcloud.to_file(output_path)

        # Display the generated word cloud using matplotlib
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title)
        plt.show()


text = lecture_dict['cs505 guest lecture  full view']
title = 'cs505 guest lecture  full view'

# Create WordCloud
wordcloud = wordcloud.generate(text)

fnameTitle = title.replace(" ", "_").replace("/", "_")
output_path = os.path.join(output_folder, f"{fnameTitle}.png")
wordcloud.to_file(output_path)

# Display the generated word cloud using matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title(title)
plt.show()

#Also generate the Word clouds for every summary
for title, summary in transcripts.items():
    # Combine title and summary text
    text = f"{title} {summary}"

    # Generate word cloud for the current title and summary
    wordcloud.generate(text)

    fnameTitle = title.replace(" ", "_").replace("/", "_")
    output_path = os.path.join(output_folder, f"{fnameTitle}.png")

    wordcloud.to_file(output_path)

    # Display the generated word cloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.show()