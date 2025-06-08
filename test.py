import requests
res = requests.get("https://api.aicu.cc/api/v3/search/getreply?uid=400482416&pn=1&ps=100&mode=0&keyword=")
print(res.json())