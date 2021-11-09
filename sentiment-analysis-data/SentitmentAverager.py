import pandas as pd
from datetime import *

# Makes the database to store the day average sentiment
SentimentAverageDF = pd.DataFrame({
    'Date': [],
    'SentimentValue': []
})

# Sentiment Data


# imports the 2018 tweet sentiment data
tweetSentiment2018 = pd.read_csv("cleaned-vader2018-2019.csv", parse_dates=['Date'])
# sorts the data
tweetSentiment2018['Date'] =pd.to_datetime(tweetSentiment2018.Date)
tweetSentiment2018.sort_values(by=['Date'], inplace=True, ascending=True)

# Stores the values needed to get an average for the day
currentDate = None
currentAmount = 0
currentSum = 0

# Loops through the database
for index, row in tweetSentiment2018.iterrows():
    # If it's none then the date has to be initiated
    if currentDate is None:
        currentDate = row["Date"];
        currentAmount += 1
        currentSum += row['0']
    # If its the same add it to the total sum for the day and increase the amount by 1
    elif currentDate == row['Date']:
        currentAmount += 1
        currentSum += row['0']
    # If its a new day then get the average and reset the variables for the next day
    else:
        sentimentAverage = currentSum / currentAmount
        SentimentAverageDF = SentimentAverageDF.append({"Date": currentDate, "SentimentValue": sentimentAverage},ignore_index=True)
        currentDate = row["Date"]
        currentAmount = 1
        currentSum = row['0']

# Adds the last day since it would exit the loop before adding it
sentimentAverage = currentSum / currentAmount
SentimentAverageDF = SentimentAverageDF.append({"Date": currentDate, "SentimentValue": sentimentAverage},ignore_index=True)
# Resets the date variable for the next loop
currentDate = None


# imports the 2019 tweet sentiment data
tweetSentiment2019 = pd.read_csv("cleaned-vader2019-2020.csv", parse_dates=['Date'])
# sorts the data
tweetSentiment2019['Date'] =pd.to_datetime(tweetSentiment2019.Date)
tweetSentiment2019.sort_values(by=['Date'], inplace=True, ascending=True)

# Loops through the database
for index, row in tweetSentiment2019.iterrows():
    # If it's none then the date has to be initiated
    if currentDate is None:
        currentDate = row["Date"];
        currentAmount += 1
        currentSum += row['0']
    # If its the same add it to the total sum for the day and increase the amount by 1
    elif currentDate == row['Date']:
        currentAmount += 1
        currentSum += row['0']
    # If its a new day then get the average and reset the variables for the next day
    else:
        sentimentAverage = currentSum / currentAmount
        SentimentAverageDF = SentimentAverageDF.append({"Date": currentDate, "SentimentValue": sentimentAverage},ignore_index=True)
        currentDate = row["Date"]
        currentAmount = 1
        currentSum = row['0']

# Adds the last day since it would exit the loop before adding it
sentimentAverage = currentSum / currentAmount
SentimentAverageDF = SentimentAverageDF.append({"Date": currentDate, "SentimentValue": sentimentAverage}, ignore_index=True)
# Resets the date variable for the next loop
currentDate = None

# imports the 2020 tweet sentiment data
tweetSentiment2020 = pd.read_csv("cleaned-vader2020-2021.csv")

# Fixed error in the data that 2021 is 2001
for index, row in tweetSentiment2020.iterrows():
    dataSplit = row["Date"].split("/")
    if dataSplit[0] == "2001":
        tweetSentiment2020.at[index, "Date"] = "2021/"+dataSplit[1]+"/" + dataSplit[2]

# sorts the data
tweetSentiment2020['Date'] = pd.to_datetime(tweetSentiment2020.Date)
tweetSentiment2020.sort_values(by=['Date'], inplace=True, ascending=True)

# Loops through the database
for index, row in tweetSentiment2020.iterrows():
    # If it's none then the date has to be initiated
    if currentDate is None:
        currentDate = row["Date"];
        currentAmount += 1
        currentSum += row['0']
    # If its the same add it to the total sum for the day and increase the amount by 1
    elif currentDate == row['Date']:
        currentAmount += 1
        currentSum += row['0']
    # If its a new day then get the average and reset the variables for the next day
    else:
        sentimentAverage = currentSum / currentAmount
        SentimentAverageDF = SentimentAverageDF.append({"Date": currentDate, "SentimentValue": sentimentAverage},ignore_index=True)
        currentDate = row["Date"]
        currentAmount = 1
        currentSum = row['0']

# Adds the last day since it would exit the loop before adding it
sentimentAverage = currentSum / currentAmount
SentimentAverageDF = SentimentAverageDF.append({"Date": currentDate, "SentimentValue": sentimentAverage},ignore_index=True)

# Exports the file to a csv
SentimentAverageDF.to_csv('C:/Users/jesse/Documents/Stuff/CodeThings/ACM/ACM_StockData/sentiment-analysis-data/{}.csv'.format("DailySentiment"))
