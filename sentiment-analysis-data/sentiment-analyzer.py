#Importing libraries
import pandas as pd
import numpy as np
import statistics
# Convention for import of the pyplot interface
import matplotlib.pyplot as plt
import contractions
#Importing packages for string manipulation!
import string
#Importing Natural Language Tool Kit
import nltk
#Importing OS to work with directories
import os
#Importing libraries needed with NLTK
from nltk import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Importing the .txt file

with open('./tweets2020-2021.csv') as reader:
    input_words = reader.readlines()

#VADER-implemented approach
analyzer = SentimentIntensityAnalyzer()
ideaFile = open("ideas.txt", "a")

sentiment_data = pd.DataFrame(columns=["sentence", "sentence_num",
                                       "sentiment","Ratio of +ve","Ratio of neutral","Ratio of -ve"])
i=1
for sentence in input_words:
    #print(sentence)
    if sentence != "\n":
        sentiment_score = analyzer.polarity_scores(sentence)
        sentiment_data.loc[len(sentiment_data.index)]=[sentence,i,sentiment_score['compound'],sentiment_score['pos'], 
                                                sentiment_score['neu'],sentiment_score['neg']]
        #print(sentiment_score)
        result = sentiment_data.to_string(index = False)
        ideaFile.write(result)

         

    i=i+1
results = ["positive","negative"]
conditions = [(sentiment_data['sentiment']>=0.05),
             (sentiment_data['sentiment']<=-0.05)]
sentiment_data['results'] = np.select(conditions, results, default="neutral")

ideaFile.close()
