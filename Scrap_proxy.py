import requests
import pandas as pd

response = requests.get("https://free-proxy-list.net/")

proxy_list = pd.read_html(response.text)[0]
proxy_list['url'] = "http://"+ proxy_list['IP Address']+ ":" + proxy_list["Port"].astype(str)
print(proxy_list.head())

https_proxies = proxy_list[proxy_list["Https"]=='yes']
print(https_proxies.count())

url = "https://httpbin.org/ip"
good_proxies = set()
headers = browser_headers["Chrome"]
for proxy_url in https_proxies["url"]:
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }
    
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=2)
        good_proxies.add(proxy_url)
        print(f"Proxy {proxy_url} OK, added to good_proxy list")
    except Exception:
        pass
    
    if len(good_proxies) >= 3:
        break


