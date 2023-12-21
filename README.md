# Summarizing Lecture Transcripts via NLP Models
We crawl publically available transcripts for NLP lectures and use pre-trained
Transformer models to summarize them, giving us digestible summaries of entire
lectures.

## To run
Clone this project and run the notebook on the `notebooks` folder. You will need
to paste your own API key for YouTube's API.

## Contents
* `summarizer.py`: main logic for crawling via YouTube's REST API and producing
                     the summaries via HuggingFace Transformer models.
* `word_clouds.py`: word cloud generation for our summaries                     
* `similarities.py`: logic to detect similarities between transcript summaries.
* `notebooks`: contains notebooks where the logic of the above files is laid out
               and ran.

**Note**: The `.py` files currently are not meant to be run but as a separation
          of logic between our project's components. To run this code see the notebooks
          section.

## Results.
See our report for a detailed explanation of our results. 


