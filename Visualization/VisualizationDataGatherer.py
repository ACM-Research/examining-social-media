import dateparser as dp
from datetime import timedelta
import pandas as pd
import math

NFLXStock = pd.read_csv("NFLX.csv")

# Removing useless columns of data
NFLXStock.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1, inplace=True)

# Querying data from 2018-09-01 to 2021-09-01
# Removing rows of data not in the time frame
for index, row in NFLXStock.iterrows():
    rowDateRaw = row['Date'];
    rowDate = dp.parse(rowDateRaw, settings={"DATE_ORDER": "YMD"})


    def removeRow():
        NFLXStock.drop(index, inplace=True)
        return

    if rowDate.year < 2018:
        removeRow()
    elif rowDate.year == 2018:
        if rowDate.month < 9:
            removeRow()
    elif rowDate.year == 2021:
        if rowDate.month >= 9:
            removeRow()


# Filling in missing values with (y + x) / 2 and repeated for other missing values

# inputs the first missing value so the code can have a starting point
NFLXStock.loc[-1] = ["2018-09-01", 365.63999939]
# Sorts by date so that the start date will be at the front
NFLXStock.sort_values(by=['Date'], inplace=True)

# Resets the index of the pandas so the index are sorted and start from 0
NFLXStock.reset_index(inplace=True)
NFLXStock.drop('index', axis=1, inplace=True)


# Loops through all the rows to fill in the missing data
for index, row in NFLXStock.iterrows():
    rowDateRaw = row['Date']
    rowDate = dp.parse(rowDateRaw, settings={"DATE_ORDER": "YMD"})

    #Catches index doesn't exist error
    try:
        someData = NFLXStock.loc[index + 1]
    except Exception:
        break

    # Gets the next date
    nextRow = NFLXStock.loc[index + 1]
    nextRowDateRaw = nextRow['Date']
    nextRowDate = dp.parse(nextRowDateRaw, settings={"DATE_ORDER": "YMD"})

    # Checks to see if there are missing dates
    if (nextRowDate - rowDate).days != 1:
        # Gets the values of the dates we have
        lastVal = row['Close']
        lastFinalVal = nextRow['Close']

        # Gets the next day that needs to be filled
        curDay = rowDate + timedelta(days=1)

        # Loops until we reach a day where we have data
        while (nextRowDate - curDay).days > 0:
            # Uses the (y + x) / 2 formula to get the missing stock value
            value = (lastVal + lastFinalVal) / 2

            # Adds 0s to the month&day if the value is less than 10(ex 8 = 08) to make sorting the array by date possbile

            curMonthStr = str(curDay.month)
            if curDay.month < 10:
                curMonthStr = "0"+ curMonthStr

            curDayStr = str(curDay.day)
            if curDay.day < 10:
                curDayStr = "0" + curDayStr

            # converts the date value to string
            curStrDate = str(curDay.year) + "-" + curMonthStr + "-" + curDayStr
            # Adds the day with it's value to the database
            curDayRow = pd.DataFrame([[curStrDate, value]], columns=["Date", "Close"])
            NFLXStock = NFLXStock.append(curDayRow, ignore_index=True)

            # Goes to the next day
            curDay = curDay + timedelta(days=1)
            lastVal = value

# Sorts by date so that all the added dates will be in order
NFLXStock.sort_values(by=['Date'], inplace=True)
# Resets the index of the pandas so the index are sorted and start from 0
NFLXStock.reset_index(inplace=True)
NFLXStock.drop('index', axis=1, inplace=True)

# renames the close column name to stock for simplicity
NFLXStock.rename(columns={"Close": "Stock"}, inplace=True)

# renames the close column name to stock for simplicity
NFLXStock.rename(columns={"Close": "Stock"}, inplace=True)

# Adding a row for change in stock

stockChangeArr = []

# Loops through all the rows to get the change for each row
for index, row in NFLXStock.iterrows():
    rowPrice = row["Stock"]

    # Catches index out of bounce error
    try:
        someData = NFLXStock.loc[index - 1]
    except Exception:
        stockChangeArr.append(0)
        continue

    beforeRowPrice = NFLXStock.loc[index - 1]['Stock']

    priceDiff = rowPrice - beforeRowPrice

    stockChangeArr.append(priceDiff)

# Adds the row
NFLXStock['StockChange'] = stockChangeArr

# adding sentiment data to the
SentimentData = pd.read_csv("../sentiment-analysis-data/sentimentAverages.csv")

# Combines stock and sentiment data into the finished dataframe
NFLXStock['Date'] = pd.to_datetime(NFLXStock.Date)
SentimentData['Date'] = pd.to_datetime(SentimentData.Date)
FinishedDF = pd.merge(NFLXStock,SentimentData, how="outer", on="Date")

# Drops rows with missing values
FinishedDF.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)

# FinishedDF['SentimentValue'] = FinishedDF['SentimentValue'] * 800;

sentimentChangeArr = []

# Loops through all the rows to get the change for each row
for index, row in FinishedDF.iterrows():
    rowSent = row["SentimentValue"]

    # Catches index out of bounce error
    try:
        someData = FinishedDF.loc[index - 1]
    except Exception:
        sentimentChangeArr.append(0)
        continue

    beforeSent = FinishedDF.loc[index - 1]['SentimentValue']

    sentDiff = rowSent - beforeSent

    sentimentChangeArr.append(sentDiff)


# Adds the row
FinishedDF['SentimentChange'] = sentimentChangeArr



# print(FinishedDF.corr())

corrArr = [];
sentimentMean = FinishedDF['SentimentValue'].mean();

for index, row in FinishedDF.iterrows():
    if row["SentimentValue"] > sentimentMean:
        if row["StockChange"] > 0:
            corrArr.append(1)
        else:
            corrArr.append(0)
    else:
        if row["StockChange"] > 0:
            corrArr.append(0)
        else:
            corrArr.append(1)

print("ALl Years Correlatoin: ", sum(corrArr) / len(corrArr))
print("All years sentiment mean: ", sentimentMean)

# Gets the index of the range for each graph,
index2018 = None;
index2019 = None;
for index, row in FinishedDF.iterrows():
    if row["Date"].year == 2019 and row["Date"].month == 9 and row["Date"].day == 1:
        index2018 = index
    elif row["Date"].year == 2020 and row["Date"].month == 9 and row["Date"].day == 1:
        index2019 = index

# Makes panda databases for each year range
year2018 = FinishedDF.iloc[:index2018, :].copy()
year2018.reset_index(inplace=True)
year2018.drop('index', axis=1, inplace=True)

year2019 = FinishedDF.iloc[:index2019, :].iloc[index2018:, :].copy()
year2019.reset_index(inplace=True)
year2019.drop('index', axis=1, inplace=True)

year2020 = FinishedDF.iloc[index2019:, :].copy()
year2020.reset_index(inplace=True)
year2020.drop('index', axis=1, inplace=True)

corrArr = [];
sentimentMean2018 = year2018['SentimentValue'].mean();

for index, row in year2018.iterrows():
    if row["SentimentValue"] > sentimentMean2018:
        if row["StockChange"] > 0:
            corrArr.append(1)
        else:
            corrArr.append(0)
    else:
        if row["StockChange"] > 0:
            corrArr.append(0)
        else:
            corrArr.append(1)

print("2018 correlation: " , sum(corrArr) / len(corrArr))
print("2018 sentiment mean: ", sentimentMean2018)

corrArr = [];
sentimentMean2019 = year2019['SentimentValue'].mean();

for index, row in year2019.iterrows():
    if row["SentimentValue"] > sentimentMean2019:
        if row["StockChange"] > 0:
            corrArr.append(1)
        else:
            corrArr.append(0)
    else:
        if row["StockChange"] > 0:
            corrArr.append(0)
        else:
            corrArr.append(1)

print("2019 correlation: ", sum(corrArr) / len(corrArr))
print("2019 sentiment mean: ", sentimentMean2019)

corrArr = [];
sentimentMean2020 = year2020['SentimentValue'].mean();

for index, row in year2020.iterrows():
    if row["SentimentValue"] > sentimentMean2020:
        if row["StockChange"] > 0:
            corrArr.append(1)
        else:
            corrArr.append(0)
    else:
        if row["StockChange"] > 0:
            corrArr.append(0)
        else:
            corrArr.append(1)

print("2020 correlation: ", sum(corrArr) / len(corrArr))
print("2020 sentiment mean: ", sentimentMean2020)


StockIncreaseBoolArr = []

for index, row in FinishedDF.iterrows():
    if row["StockChange"] > 0:
        StockIncreaseBoolArr.append(1)
    else:
        StockIncreaseBoolArr.append(0)

FinishedDF['StockIncreaseBool'] = StockIncreaseBoolArr

SentimentPositiveBoolArr = []

for index, row in FinishedDF.iterrows():
    if row["SentimentValue"] > sentimentMean:
        SentimentPositiveBoolArr.append(1)
    else:
        SentimentPositiveBoolArr.append(0)

FinishedDF['SentimentPositiveBool'] = SentimentPositiveBoolArr

# Exports the panda database to a file
FinishedDF.to_csv('C:/Users/jesse/Documents/Stuff/CodeThings/ACM/ACM_StockData/Visualization/{}.csv'.format("VisualizationData"))

FinishedDF.corr().to_csv('C:/Users/jesse/Documents/Stuff/CodeThings/ACM/ACM_StockData/Visualization/{}.csv'.format("CorrelationThings"))