from bokeh.plotting import figure, output_file, show
import pandas as pd

# gets the data for visualization
VisualizationData = pd.read_csv("VisualizationData.csv", parse_dates=['Date'])

# Reduces the stock change value into a range of -1 to 1 to match sentiment value
for index, row in VisualizationData.iterrows():
    VisualizationData.at[index,"StockChange"] =  max(-1,min(row["StockChange"]/ 25 ,1));

# Makes the graph object
p = figure(
    title='Sentiment & Stock',
    x_axis_label='Date',
    y_axis_label='Value',
    plot_width=800,
    plot_height=600,
    x_axis_type='datetime'
)

# Adds a line for the stock values
p.line(VisualizationData["Date"], VisualizationData["StockChange"], legend_label="StockData", line_width=2, line_color="Red")

# Adds a line for the sentiment values
p.line(VisualizationData["Date"], VisualizationData["SentimentValue"], legend_label="Sentiment", line_width=2, line_color="Blue")

show(p)
