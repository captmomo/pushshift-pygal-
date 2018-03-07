# pushshift-pygal-

Hacky script to plot pygal charts using data from pushshift.

## Getting the data

Data is taken from [pushshift](https://elastic.pushshift.io/).  
Guide on how to formulate a query can be found [here](https://elastic.pushshift.io/)

For checking purposes, I found it easier to formulate the query in the browser till you get the results you want and just paste the url into the script. Rather than doing the conventional method of building out the params and then performing the request and checking the json response.  
  
For this dataset, I used the following search parameters:

Complete url:
https://elastic.pushshift.io/rs/submissions/_search/?q=(title:/r/singapore%20random%20discussion%20and%20small%20questions%20thread%20AND%20created_utc:>1514750000%20AND%20author:automoderator%20AND%20subreddit:singapore)&sort=created_utc:desc&size=500

Breakdown:

q=(title:/r/singapore random discussion and small questions thread AND created_utc:>1514750000 AND author:automoderator AND subreddit:singapore)

created_utc is in seconds from epoch

Sorted in chronological order, latest first and a search result limit of 500.

Once you are satisfied with the results, use requests to pull it  
  
    import requests
    
    url = 'enter your url here'
    res = requests.get(url)
    data = res.json()
    
The data you are most likely interested in is located in data['hits']['hits']

    results = data['hits']['hits']
    #check the data and get only the stuff you are interested in. for my case, I only want results from the subreddit singapore.
    threads = []
    for item in results:
        subreddit = item['_source']['subreddit']
        if subreddit == 'singapore':
            threads.append(item['_source'])
     
    #write to json file:
    with open('output.json', 'w+', encoding='utf-8') as f:
        json.dump(threads, f)
        
 Next step will be to load the json using pandas and then plotting it using pygal.










