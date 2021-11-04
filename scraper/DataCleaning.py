import csv
import re
import html

f1 = open('tweets2019-2020.csv')
csv_f1 = csv.reader(f1)

tweet_list = []
tweet_list_dates = []

for row in csv_f1:
    tweet_list.append(row[0])
#  All the tweets are now stored in a list

f2 = open("tweets2019-2020.csv")
csv_f2 = csv.reader(f2)

for row in csv_f2:
    tweet_list_dates.append(row[1])
print(tweet_list_dates)

# converting all tweets to lowercase
for i in range(len(tweet_list)):
    temp = tweet_list[i].lower()
    tweet_list[i] = temp
# all dates of the tweets are now stored in a list

# Removing links
for i in range(len(tweet_list)):
    edited_temp = tweet_list[i]
    edited_temp = tweet_list[i].replace("\n", " ")     # remove new line char
    edited_temp = re.sub(r"http\S+", "", edited_temp)  # remove links
    edited_temp = re.sub(r"www.\S+", "", edited_temp)
    tweet_list[i] = edited_temp

for i in range(len(tweet_list)):  # remove hashtags
    tweet_list[i] = re.sub(r"(@[A-Za-z0-9] +)| [^\w\s]|#|http\S+", " ", tweet_list[i])

for i in range(len(tweet_list)):  # removing digits
    string = tweet_list[i]
    new_string = ''.join([i for i in string if not i.isdigit()])
    tweet_list[i] = new_string


for i in range (len(tweet_list)):  # removing other special char
    tweet = tweet_list[i]
    edited = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    tweet_list[i] = edited

# Removing stopwords
from gensim.parsing.preprocessing import remove_stopwords
for i in range(len(tweet_list)):
    text = tweet_list[i]
    filtered_sentence = remove_stopwords(text)
    tweet_list[i] = filtered_sentence


# Writing list to a new CSV file
from itertools import zip_longest
d = [tweet_list, tweet_list_dates]
export_data = zip_longest(*d, fillvalue = '')
with open('edited_tweets2019-2020.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow(("Edited tweets", "Date"))
      wr.writerows(export_data)
myfile.close()