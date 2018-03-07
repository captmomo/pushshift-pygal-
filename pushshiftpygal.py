import pandas as pd
import json
import pygal
import time

#create dataframe from json file
df = pd.read_json('output.json', orient='records')

#convert epoch time to utc and timeshift to local Singapore time
df['created_utc'] = pd.to_datetime(df['created_utc'],unit='s') + pd.Timedelta('08:00:00')

def scatter():
    '''plots scatter chart'''
    xy_chart = pygal.DateTimeLine(stroke=False, show_legend=False, x_label_rotation=35)
    xy_chart.title = "/r/singapore daily thread post count 1st Jan - 6 Mar 18"
    xy_chart.x_title = "Date"
    xy_chart.y_title = "Comments"
    for index, item in df.iterrows():
        xy_chart.add(item['created_utc'], [
            {'value': (item['created_utc'],  item['num_comments']), 
            'label':'Score: {0}'.format(item['score']),
            'xlink': item['url']}])
    xy_chart.render_in_browser()

def linechart():
    '''plots line chart'''
    xy_chart = pygal.DateTimeLine(x_label_rotation=35, show_legend=False)
    xy_chart.title = "/r/singapore daily thread comment count 1st Jan - 6 Mar 18"
    xy_chart.x_title = "Date"
    xy_chart.y_title = "Comments"
    #zip columns to create list of tuples for values to plot
    values = []
    for index, item in df.iterrows():
        value = (item['created_utc'],  item['num_comments'])
        label = 'Score: {0}'.format(item['score'])
        values.append({ 'value' : value, 'label': label, 'xlink': item['url']})
    #values = list(zip(df.created_utc, df.num_comments))
    xy_chart.add('series', values)
    xy_chart.render_in_browser()

linechart()
