import dateparser as dp
from datetime import timedelta
import pandas as pd
import math
from bokeh.plotting import figure, output_file, show

# Querying data from 2018-09-01 to 2021-09-01

NFLXStock = pd.read_csv("NFLX.csv")

# Removing useless columns of data
NFLXStock.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1, inplace=True)

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

changeArr = []

# Loops through all the rows to get the change for each row
for index, row in NFLXStock.iterrows():
    rowPrice = row["Stock"]

    # Catches index out of bounce error
    try:
        someData = NFLXStock.loc[index - 1]
    except Exception:
        changeArr.append(0)
        continue

    beforeRowPrice = NFLXStock.loc[index - 1]['Stock']

    priceDiff = rowPrice - beforeRowPrice

    changeArr.append(priceDiff)

# Adds the row
NFLXStock['StockChange'] = changeArr

# Adding temporary sentiment data

sentimentVals = []

for index, row in NFLXStock.iterrows():
    sentiVal = math.sin(index * math.pi /100)

    sentimentVals.append(sentiVal)

NFLXStock['SentimentValue'] = sentimentVals

# Exports the panda database to a file
NFLXStock.to_csv('C:/Users/jesse/Documents/Stuff/CodeThings/ACM/ACM_StockData/{}.csv'.format("VisualizationData"))
