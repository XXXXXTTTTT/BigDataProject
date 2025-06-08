import requests

url = 'https://api.aicu.cc/api/v3/search/getreply?uid=400482416&pn=1&ps=100&mode=0&keyword='

response = requests.get(url)
print(response.text)