from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import pandas as pd

# Gets the data for visualization
VisualizationData = pd.read_csv("VisualizationData.csv", parse_dates=['Date'])

# Removes useless row
VisualizationData.drop('Unnamed: 0', axis=1, inplace=True)

# Reduces the stock change value into a range of -1 to 1 to match sentiment value
for index, row in VisualizationData.iterrows():
    VisualizationData.at[index, "StockChange"] = max(-1, min(row["StockChange"] / 25, 1))

# Gets the index of the range for each graph,
index2018 = None;
index2019 = None;
for index, row in VisualizationData.iterrows():
    if row["Date"].year == 2019 and row["Date"].month == 9 and row["Date"].day == 1:
        index2018 = index
    elif row["Date"].year == 2020 and row["Date"].month == 9 and row["Date"].day == 1:
        index2019 = index

# Makes panda databases for each year range
year2018 = VisualizationData.iloc[:index2018, :].copy()
year2018.reset_index(inplace=True)
year2018.drop('index', axis=1, inplace=True)

year2019 = VisualizationData.iloc[:index2019, :].iloc[index2018:, :].copy()
year2019.reset_index(inplace=True)
year2019.drop('index', axis=1, inplace=True)

year2020 = VisualizationData.iloc[index2019:, :].copy()
year2020.reset_index(inplace=True)
year2020.drop('index', axis=1, inplace=True)

# Makes the graph object for stock 2018
stockYear2018 = figure(
    title='Stock(9/2018-9/2019)',
    x_axis_label='Date',
    y_axis_label='Stock Value($)',
    plot_width=500,
    plot_height=500,
    x_axis_type='datetime',
    y_range=(0, 600)
)

# Adds a line for the stock values
stockYear2018.line(year2018["Date"], year2018["Stock"], legend_label="StockData", line_width=2,
                   line_color="Red")

# Makes the graph object for stock 2019
stockYear2019 = figure(
    title='Stock(9/2019-9/2020)',
    x_axis_label='Date',
    y_axis_label='Stock Value($)',
    plot_width=500,
    plot_height=500,
    x_axis_type='datetime',
    y_range=(0, 600)
)

# Adds a line for the stock values
stockYear2019.line(year2019["Date"], year2019["Stock"], legend_label="StockData", line_width=2,
                   line_color="Orange")

# Makes the graph object for stock 2020
stockYear2020 = figure(
    title='Stock(9/2020-9/2021)',
    x_axis_label='Date',
    y_axis_label='Stock Value($)',
    plot_width=500,
    plot_height=500,
    x_axis_type='datetime',
    y_range=(0, 600)
)

# Adds a line for the stock values
stockYear2020.line(year2020["Date"], year2020["Stock"], legend_label="StockData", line_width=2,
                   line_color="Yellow")

# Makes the graph object for sentiment 2018
sentimentYear2018 = figure(
    title='Sentiment(9/2018-9/2019)',
    x_axis_label='Date',
    y_axis_label='Sentiment Value',
    plot_width=500,
    plot_height=500,
    x_axis_type='datetime',
    y_range=(-1, 1)
)

# Adds a line for the stock values
sentimentYear2018.line(year2018["Date"], year2018["SentimentValue"], legend_label="SentimentData", line_width=2,
                       line_color="Red")

# Makes the graph object for sentiment 2019
sentimentYear2019 = figure(
    title='Sentiment(9/2019-9/2020)',
    x_axis_label='Date',
    y_axis_label='Sentiment Value',
    plot_width=500,
    plot_height=500,
    x_axis_type='datetime',
    y_range=(-1, 1)
)

# Adds a line for the stock values
sentimentYear2019.line(year2019["Date"], year2019["SentimentValue"], legend_label="SentimentData", line_width=2,
                       line_color="Orange")

# Makes the graph object for sentiment 2020
sentimentYear2020 = figure(
    title='Sentiment(9/2020-9/2021)',
    x_axis_label='Date',
    y_axis_label='Sentiment Value',
    plot_width=500,
    plot_height=500,
    x_axis_type='datetime',
    y_range=(-1, 1)
)

# Adds a line for the stock values
sentimentYear2020.line(year2020["Date"], year2020["SentimentValue"], legend_label="SentimentData", line_width=2,
                       line_color="Yellow")

# Makes the graph object for sentiment and stock together for 2018
SentimentnStock2018 = figure(
    title='Sentiment and Stock(9/2018 - 9/2019)',
    x_axis_label='Date',
    y_axis_label='Value',
    plot_width=500,
    plot_height=500,
    x_axis_type='datetime',
    y_range=(-1, 1)
)

# Adds a line for the stock values
SentimentnStock2018.line(year2018["Date"], year2018["StockChange"], legend_label="StockData", line_width=2,
                         line_color="Red")

# Adds a line for the sentiment values
SentimentnStock2018.line(year2018["Date"], year2018["SentimentValue"], legend_label="Sentiment", line_width=2,
                         line_color="Blue")

# Makes the graph object for sentiment and stock together for 2019
SentimentnStock2019 = figure(
    title='Sentiment and Stock(9/2019 - 9/2020)',
    x_axis_label='Date',
    y_axis_label='Value',
    plot_width=500,
    plot_height=500,
    x_axis_type='datetime',
    y_range=(-1, 1)
)

# Adds a line for the stock values
SentimentnStock2019.line(year2019["Date"], year2019["StockChange"], legend_label="StockData", line_width=2,
                         line_color="Red")

# Adds a line for the sentiment values
SentimentnStock2019.line(year2019["Date"], year2019["SentimentValue"], legend_label="Sentiment", line_width=2,
                         line_color="Blue")


# Makes the graph object for sentiment and stock together for 2020
SentimentnStock2020 = figure(
    title='Sentiment and Stock(9/2020 - 9/2021)',
    x_axis_label='Date',
    y_axis_label='Value',
    plot_width=500,
    plot_height=500,
    x_axis_type='datetime',
    y_range=(-1, 1)
)

# Adds a line for the stock values
SentimentnStock2020.line(year2020["Date"], year2020["StockChange"], legend_label="StockData", line_width=2,
                         line_color="Red")

# Adds a line for the sentiment values
SentimentnStock2020.line(year2020["Date"], year2020["SentimentValue"], legend_label="Sentiment", line_width=2,
                         line_color="Blue")

# Puts all the graphs into a dictionary so we can embed them all at the same time
Graphs = {"Stock2018": stockYear2018,"Stock2019": stockYear2019,"Stock2012": stockYear2020}

# Gets the embedding code
script, divs = components(Graphs)

# Exports the embedded javascript code into a file
ScriptFile = open("/Scripts.txt", "w")
ScriptFile.write(script)
ScriptFile.close()

# Exports the embedded html div code into a file
DivFile = open("/Divs.txt", "w")
DivFile.write(str(divs))
DivFile.close()