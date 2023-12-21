# File : summarizer.py

# Description: contains logic for fetching and summarizing youtube transcripts

# Date: December 2023

# Authors: Themistoklis Haris, Themistoklis Nikas


API_KEY = "##"  # Replace with your valid YouTube Data API key

# Define the channel ID
channel_id = "UCfSqNB0yh99yuG4p4nzjPOA"  # Replace with the desired channel ID

def get_video_info(channel_id):
    """
    Gets a list of video IDs and corresponding video titles from a YouTube channel.

    Args:
        channel_id: The ID of the YouTube channel.

    Returns:
        A list of tuples containing video IDs and corresponding video titles.
    """
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    # Get the channel's upload playlist ID
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id,
    )
    response = request.execute()
#     print(response)
    playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Get videos from the upload playlist
    videos = {}
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token,
        )
        response = request.execute()

        for item in response["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            video_title = item["snippet"]["title"]
            videos[video_title] = video_id
#             video_info_list.append((video_id, video_title))

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos

# Get the video IDs and titles
videos = get_video_info(channel_id)

# Print the video IDs and titles
print(f"Video IDs and Titles for channel {channel_id}:")
for video_title, video_id in videos.items():
    print(f"- Title: {video_title}, Video ID: {video_id}")

miscellaneous = {}
slide_view = {}
full_view = {}
singles = {}
for title, v_id in videos.items():
    title = title.lower()
    if "lecture" in title:
        if 'slide view' in title:
            slide_view[title] = v_id
        elif 'full view' in title:
            full_view[title] = v_id
        else:
            singles[title] = v_id
    else:
        miscellaneous[title] = v_id

transcripts = {}

for title, video_id in videos.items():

    text = ""

    # Experiment: last video
    try:

        # Get the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Append all the entries to a single text. Add newlines between different
        # parts to make post-processing easier later.
        for entry in transcript:

            # Remove certain unnecessary words and get the text we need to retain.
            txt = entry['text'].replace("uh", "")
            txt = txt.replace("um", "")

            text += (" " + txt)

        print(len(text))

        # Append to our list of transcripts.
        transcripts[title] = text

    # Ignore failures.
    except Exception as e:
        print("Some error happened. Skipping this transcript", title, video_id)

# The text comes in quite an unprocessed way.
# It is really difficult to be accurate in separating it into sentences,
# so we can use this library to get somewhat of an approximation!

def process_transcript(i):

    text = transcripts[i]

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Get the list of sentences.
    sentences = [sentence.text + "." for sentence in doc.sents]
    print (len(sentences))

    # Now we need to pair up shorter sentences in order to minimize the number of
    # times we'll need to call our model.
    sentences_post = []

    i = 0
    while i < len(sentences):

        s = ""

        while i < len(sentences):

            if len(s) + len(sentences[i]) >= 400:

                if s == "":
                    i = i + 1

                break

            s += (sentences[i] + " ")
            i += 1

        # Only keep large sentences.
        if s != "" and len(s) >= 250:
            sentences_post.append(s)

    return sentences_post

  # for sent in sentences_post:
  #   print(f"{len(sent)} -> {sent}")

def get_summary(i):

  # IDEA 1: try to append current summary with next sentence to summarize the entire lecture.
  # VERDICT: This doesn't work very well. The model just keeps previous information and forgets
  #          about new one.

  # IDEA 2: Summarize in layers. First summarize every sentence with small sentences,
  #         then summarize batches of those and so on.

    sentences_post = process_transcript(i)

    summaries = []

    i = 0
    for sent in sentences_post:

        if i % 5 == 0:
            print(f"Progress: {i/float(len(sentences_post))*100}%")

        summaries.append(generatorStageOne("summarize: " + sent)[0]["summary_text"])

        i += 1

    print("Stage 1: DONE")

    summaries2 = []

    j = 0
    while j < len(summaries):

        if j + 2 < len(summaries):
            sent = summaries[j] + " " + summaries[j + 1] + summaries[j + 2]
        elif j + 1 < len(summaries):
            sent = summaries[j] + " " + summaries[j + 1]
        else:
            sent = summaries[j]

        summaries2.append(generatorStageOne("summarize: " + sent)[0]["summary_text"])

        j += 3

    print("Stage 2: DONE")


    summary = ""

    j = 0
    while j < len(summaries2):

        if j + 2 < len(summaries2):
            sent = summaries2[j] + " " + summaries2[j + 1] + summaries2[j + 2]
        elif j + 1 < len(summaries2):
            sent = summaries2[j] + " " + summaries2[j + 1]
        else:
            sent = summaries2[j]

        summary += (generatorStageTwo("summarize: " + sent)[0]["summary_text"] + "")

        j += 3

    print("DONE")
    return summary

summaries = []

model = 'sshleifer/distilbart-cnn-12-6'
modelName = 'distilBart'

generatorStageOne = pipeline('summarization',
                        model=model,
                        max_length=50)

generatorStageTwo = pipeline('summarization',
                        model=model,
                        max_length=30)

# for i in range(len(transcripts)):
for title in transcripts.keys():
    print(f"Transcript: {title}")
    summary = get_summary(title)
    print(summary)
    # Append summary to file.
    with open("./summaries"+modelName+".txt", "a") as file:
        file.write(f"{title}\n" + summary + "\n\n")

lectures = []
for key in full_view.keys():
    match = re.match(r'.*lecture (\d+).*', key)
    if match:
        lecture_number = match.group(1)
        lecture_string = f"lecture {lecture_number}"
        for k in slide_view.keys():
            if lecture_string in k and 'guest' not in k:
                lectures.append((key, k))
#         print(f"Key: {key}, {lecture_string}")
for key in full_view.keys():
    for k in slide_view.keys():
        if 'guest' in key and 'guest' in k:
            lectures.append((key, k))
            break
