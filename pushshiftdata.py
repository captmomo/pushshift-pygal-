import requests
import json
    
url = 'https://elastic.pushshift.io/rs/submissions/_search/?q=(title:/r/singapore%20random%20discussion%20and%20small%20questions%20thread%20AND%20created_utc:>1514750000%20AND%20author:automoderator%20AND%20subreddit:singapore)&sort=created_utc:desc&size=500'
res = requests.get(url)
data = res.json()

results = data['hits']['hits']
#check the data and get only the stuff you are interested in. For this example, I only want results from the subreddit singapore.
threads = []
for item in results:
    subreddit = item['_source']['subreddit']
    if subreddit == 'singapore':
        threads.append(item['_source'])

with open('output.json', 'w+', encoding='utf-8') as f:
    json.dump(threads, f)