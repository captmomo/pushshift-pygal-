# pushshift-pygal-

Hacky script to plot pygal charts using data from pushshift.

## Getting the data

Data is taken from [pushshift](https://elastic.pushshift.io/).  
Guide on how to formulate a query can be found [here](https://elastic.pushshift.io/)

For checking purposes, I found it easier to formulate the query in the browser till you get the results you want and just paste the url into the script. Rather than doing the conventional method of building out the params and then performing the request and checking the json response.  
  
For this dataset, I used the following search parameters:

Complete url:
https://elastic.pushshift.io/rs/submissions/_search/?q=(title:/r/singapore%20random%20discussion%20and%20small%20questions%20thread%20AND%20created_utc:>1514750000%20AND%20author:automoderator%20AND%20subreddit:singapore)&sort=created_utc:desc&size=500

### Breakdown:

q=(title:/r/singapore random discussion and small questions thread AND created_utc:>1514750000 AND author:automoderator AND subreddit:singapore)

created_utc is in seconds from epoch

Sorted in chronological order, latest first and a search result limit of 500.

### Using requests

Once you are satisfied with the results, use requests to pull it  
  
    import requests
    import json
    
    url = 'enter your url here'
    res = requests.get(url)
    data = res.json()
    
The data you are most likely interested in is located in data['hits']['hits']

    results = data['hits']['hits']
    #check the data and get only the stuff you are interested in. for my case, I only want results from the subreddit singapore.
    threads = []
    for item in results:
        #the info I want is located in '_source'
        subreddit = item['_source']['subreddit']
        if subreddit == 'singapore':
            threads.append(item['_source'])
     
    #write to json file:
    with open('output.json', 'w+', encoding='utf-8') as f:
        json.dump(threads, f)
        
 Next step will be to load the json using pandas and then plotting it using pygal.
 
 ## Plotting with pygal and pandas
 
 First, load the json into a dataframe use pandas read_json function.

    import pandas as pd
    import pygal
    
    df = pd.read_json('output.json', orient='records')
 
Next we'll use pd.to_datetime to convert the time from seconds since epoch (UTC/GMT) to a proper human readable date time. If you wish to offset the time to your local time use pd.time_delta. For my example, I'll be using +8 hours.
 
     df['timestamp'] = pd.to_datetime(df['created_utc'],unit='s') + pd.Timedelta(hours=8)
     
Since this is a time series, I'll be using [pygal.DateTimeLine()](http://www.pygal.org/en/stable/documentation/types/xy.html) 
In the pushshiftpygal.py, I provided 2 examples - scatter and line chart. 

The 2 main differences are:

* setting stroke=False for the scatter plot
* defining the values to plot

### Line chart

For the line chart, I created a list of dicts:

    values =[]
    for index, item in df.iterrows():
        value = (item['timestamp'],  item['num_comments'])
        label = 'Score: {0}'.format(item['score'])
        values.append({ 'value' : value, 'label': label, 'xlink': item['url']})

value is a tuple - (x_coordinate, y_coordinate)
label is the text in the popup when you hover over the point - you can exclude this if you don't see a need for it.
xlink is for you to input a url that the user can click when they hover over the point
For the complete options check out [pygal docs](http://www.pygal.org/en/stable/documentation/configuration/value.html)

Finally create the chart. The current script renders in your browser. You can also save it to a [svg file, png image or a base64 data uri. Check out the docs for the complete set of options](http://www.pygal.org/en/stable/documentation/output.html)

    xy_chart = pygal.DateTimeLine(x_label_rotation=35, show_legend=False)
    xy_chart.title = "/r/singapore daily thread comment count 1st Jan - 6 Mar 18"
    xy_chart.x_title = "Date"
    xy_chart.y_title = "Comments"
    xy_chart.add('series name', values)
    xy_chart.render_in_browser()
    
 The end product can be viewed [here])(http://bl.ocks.org/captmomo/86566acc4b572fe3663c74a0a97f6aa8)







