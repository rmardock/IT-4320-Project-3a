'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
from time import time
import json
import requests
import pygal
import datetime

# Function to query api
def query_API(time_series, symbol, key):
    # Build url 
    if(time_series == "TIME_SERIES_INTRADAY"):
        # URL for Intraday Time Series
        url = "https://www.alphavantage.co/query?function=" + time_series + "&symbol=" + symbol + "&interval=5min&outputsize=full&apikey=" + key
    else:
        # URL for all other Time Series selections
        url = "https://www.alphavantage.co/query?function=" + time_series + "&symbol=" + symbol + "&outputsize=full&apikey=" + key
    response = requests.request("GET", url)
    data = response.json()
    return data

# Function to parse data 
def parse_data(data, time_series, date):
    # Cast date as string for parsing JSON
    date = str(date)
    try: 
        open = data[time_series][date]["1. open"]
        high = data[time_series][date]["2. high"]
        low = data[time_series][date]["3. low"]
        close = data[time_series][date]["4. close"]
    # If no data is present, assign None
    except KeyError:
        open = None
        close = None
        low = None
        high = None
    return open, high, low, close

# Function to format time series for use
def format_time_series(time_series):
    if(time_series == "1"):
        return "Time Series (5min)", "TIME_SERIES_INTRADAY"
    elif(time_series == "2"):
        return "Time Series (Daily)", "TIME_SERIES_DAILY_ADJUSTED"
    elif(time_series == "3"):
        return "Weekly Time Series", "TIME_SERIES_WEEKLY"
    elif(time_series == "4"):
        return "Monthly Time Series", "TIME_SERIES_MONTHLY"

# Function to build chart 
def build_chart(symbol, chart_type, data, time_series, start_date, end_date):
    i = 0
    # Variables for assigning user selected start and end dates to graph title
    tmp_start = start_date
    tmp_end = end_date
    
    # Build string for graph title
    graph_title = "Stock Data for " + symbol + ": " + str(tmp_start) + " to " + str(tmp_end)
    
    # Initialize lists to store data points
    open_list = []
    close_list = []
    high_list = []
    low_list = []
    date_list = []
    
    # If intraday time series is selected, format date and time and assign delta
    if(time_series == "Time Series (5min)"):
        start_date = datetime.datetime.strptime(str(start_date) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_date = datetime.datetime.strptime(str(end_date) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        delta = datetime.timedelta(minutes=5)
    else:
        # If not intraday, assign delta here
        delta = datetime.timedelta(days=1)
    
    # If chart selection is line chart  
    if(chart_type == "2"): 
        chart = pygal.Line()
    
    # If chart selection is bar chart
    if(chart_type == "1"):
        chart = pygal.Bar()
    
    # If neither chart is selected
    elif(chart_type != "1" and chart_type != "2"):
        # Handle errors here 
        print("ERROR! Chart selection invalid!")
        chart = None
        return chart
    
    # While loop for iterating through dates between the start and end date supplied by the user
    while(start_date <= end_date):
        # Parse data for each iteration 
        open, high, low, close = parse_data(data, time_series, start_date)
        # If no data is present, skip this iteration and continue on to the next
        if(open == None and high == None and low == None and close == None):
            # Increment date
            start_date += delta
            continue
        
        # Add data to lists 
        open_list.append(float(open))
        close_list.append(float(close))
        high_list.append(float(high))
        low_list.append(float(low))
        date_list.append(start_date)
        # Increment date
        start_date += delta
    
    # Add data to the chart from populated lists
    chart.add("Open", open_list)
    chart.add("Close", close_list)
    chart.add("High", high_list)
    chart.add("Low", low_list)
    
    # Assign chart title
    chart.title = graph_title
    # Assign chart labels
    chart.x_labels = date_list
    # Return chart
    return chart.render_data_uri()

# Function to get stock symbols from json files
def get_symbols(symbol_choices, path, key):
    # Open json file
    file = open(path)
    # Assign json to variable
    data = json.load(file)
    # Iterate json
    for i in data:
        # Build symbol tuples and add to list 
        symbol_choices.append((i[key], i[key]))
    # Close json file
    file.close()
    # Return list
    return symbol_choices

#Helper function for converting date
def convert_date(str_date):
    return datetime.datetime.strptime(str_date, '%Y-%m-%d').date()