import requests

# API URL
url = "https://api.aicu.cc/api/v3/search/getreply"

# 请求参数
params = {
    'uid': '400482416',
    'pn': '1',
    'ps': '100',
    'mode': '0',
    'keyword': ''
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    print("状态码:", response.status_code)
    print("响应内容:", response.json())
    
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")