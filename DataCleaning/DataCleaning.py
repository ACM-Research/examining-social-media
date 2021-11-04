import csv
import re

# The data will keep its original casing and punctuation marks which will convey motions.

tweet_list = []
tweet_list_dates = []

f1 = open('tweets2020-2021.csv')
csv_f1 = csv.reader(f1)
# Storing tweets in a list
for row in csv_f1:
    tweet_list.append(row[0])
tweet_list.pop(0) # removing the top header

f2 = open("tweets2020-2021.csv")
csv_f2 = csv.reader(f2)
# Storing tweets in a list
for row in csv_f2:
    tweet_list_dates.append(row[1])
print(tweet_list_dates)

# converting all tweets to lowercase
for i in range(len(tweet_list)):
    temp = tweet_list[i].lower()
    tweet_list[i] = temp
# all dates of the tweets are now stored in a list

# Removing links
tweet_list_dates.pop(0) # removing the top header

# Removing links from tweets
for i in range(len(tweet_list)):
    edited_temp = tweet_list[i]
    edited_temp = tweet_list[i].replace("\n", " ")  # remove new line char
    edited_temp = re.sub(r"http\S+", "", edited_temp)  # remove links
    edited_temp = re.sub(r"www.\S+", "", edited_temp)
    edited_temp = edited_temp.replace(".com", "").replace("Com", "").replace(".COM", "").replace(".net", "").replace(".org", "") .replace(".be", "").replace(".de", "")# removing other links that are not HTTPS
    tweet_list[i] = edited_temp

for i in range(len(tweet_list)):  # remove hashtags
    tweet_list[i] = re.sub(r"(@[A-Za-z0-9] +)| [^\w\s]|#|http\S+", " ", tweet_list[i])

for i in range(len(tweet_list)):  # removing digits
    string = tweet_list[i]
    new_string = ''.join([i for i in string if not i.isdigit()])
    tweet_list[i] = new_string

for i in range(len(tweet_list)):  # removing some other symbols
    tweet = tweet_list[i]
    edited_temp = re.sub("[$%*@()<>{}|]", "", tweet)
    edited_temp = edited_temp.replace("\\", "").replace("/", "")
    tweet_list[i] = edited_temp

# Removing stopwords
from gensim.parsing.preprocessing import remove_stopwords

for i in range(len(tweet_list)):
    text = tweet_list[i]
    filtered_sentence = remove_stopwords(text)
    tweet_list[i] = filtered_sentence

# Removing all instances of "replying to" in a tweet
for i in range(len(tweet_list)):
    tweet_list[i] = tweet_list[i].replace("reply to", "").replace("Reply to", "").replace("replying to", "").replace(
        "Replying to", "").replace("replying", "").replace("Replying", "").replace("reply", "").replace("Reply", "")

#   Writing list to a CSV file
import pandas as pd
dictionary = {'Edited tweets': tweet_list, 'Date': tweet_list_dates}
dataframe = pd.DataFrame(dictionary)
dataframe.to_csv("cleaned_tweets20-21.csv")
