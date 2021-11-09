import pandas as pd
from collections import defaultdict
from datetime import *


def average_tweet_sentiments(csv_file):
    dataframe = pd.DataFrame({
        'Date': [],
        'SentimentValue': []
    })

    values_by_date = defaultdict(list)

    for _, file_row in csv_file.iterrows():
        values_by_date[file_row['Date']].append(file_row['0'])

    averages_by_date = {k: sum(l) / len(l) for k, l in values_by_date.items()}
    key_list = list(averages_by_date.keys())
    val_list = list(averages_by_date.values())

    dataframe['Date'] = key_list
    dataframe['SentimentValue'] = val_list

    return dataframe


# Makes the database to store the day average sentiment
SentimentAverageDF = pd.DataFrame({
    'Date': [],
    'SentimentValue': []
})

# imports the 2018 tweet sentiment data
tweetSentiment2018 = pd.read_csv("cleaned-vader2018-2019.csv", parse_dates=['Date'])
# sorts the data
tweetSentiment2018['Date'] = pd.to_datetime(tweetSentiment2018.Date)
tweetSentiment2018.sort_values(by=['Date'], inplace=True, ascending=True)

df2018 = average_tweet_sentiments(tweetSentiment2018)

# imports the 2019 tweet sentiment data
tweetSentiment2019 = pd.read_csv("cleaned-vader2019-2020.csv", parse_dates=['Date'])
# sorts the data
tweetSentiment2019['Date'] = pd.to_datetime(tweetSentiment2019.Date)
tweetSentiment2019.sort_values(by=['Date'], inplace=True, ascending=True)

df2019 = average_tweet_sentiments(tweetSentiment2019)

# imports the 2020 tweet sentiment data
tweetSentiment2020 = pd.read_csv("cleaned-vader2020-2021.csv")

# Fixed error in the data that 2021 is 2001
for index, row in tweetSentiment2020.iterrows():
    dataSplit = row['Date'].split("/")
    if dataSplit[0] == "2001":
        tweetSentiment2020.at[index, "Date"] = "2021/" + dataSplit[1] + "/" + dataSplit[2]

# sorts the data
tweetSentiment2020['Date'] = pd.to_datetime(tweetSentiment2020.Date)
tweetSentiment2020.sort_values(by=['Date'], inplace=True, ascending=True)

df2020 = average_tweet_sentiments(tweetSentiment2020)

SentimentAverageDF = pd.concat([df2018, df2019, df2020])

# Exports the file to a csv
SentimentAverageDF.to_csv('C:/Users/jluo1/OneDrive/Documents/sentimentAverages.csv', index=False)
