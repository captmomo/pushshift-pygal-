import json

import pygal
import pandas as pd

def main():
    #load and create dataframe
    df = load_json('output.json', hours=8)
    #plot points
    scatter(df)

def load_json(infile, hours=0):
    '''create dataframe from json file and offset time'''
    df = pd.read_json(infile, orient='records')
    #convert epoch time to utc and timeshift to local Singapore time
    df['timestamp'] = pd.to_datetime(df['created_utc'],unit='s') + pd.Timedelta(hours=hours)
    return df

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
    #create list of dict for values to plot
    values = []
    for index, item in df.iterrows():
        value = (item['created_utc'],  item['num_comments'])
        label = 'Score: {0}'.format(item['score'])
        values.append({ 'value' : value, 'label': label, 'xlink': item['url']})
    xy_chart.add('series', values)
    xy_chart.render_in_browser()
