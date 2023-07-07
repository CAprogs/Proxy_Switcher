import requests
import pandas as pd
import yaml
import time
from selenium import webdriver

#############################################################################################################################
############################################### HEADERS #####################################################################
# Chargement des headers
with open("/Users/charles-albert/Desktop/Manga Downloader/Proxy Headers/headers.yml") as f_headers:
    browser_headers = yaml.safe_load(f_headers)
print('\n',browser_headers["Firefox"])

response = requests.get("https://httpbin.org/headers", headers=browser_headers["Firefox"])
time.sleep(5)
print('\n',response.json())

#############################################################################################################################
################################################## PROXIES ##################################################################

def Good_proxies(https_proxies):

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
    
    return good_proxies
    
response_1 = requests.get("https://free-proxy-list.net/")           # 1er Site

print("\nScrapping Proxies 1 : ")
# récupérer la liste des free proxies 
proxy_list_1 = pd.read_html(response_1.text)[0]
proxy_list_1['url'] = "http://"+ proxy_list_1['IP Address']+ ":" + proxy_list_1["Port"].astype(str)
print('\n',proxy_list_1.head())

# Liste des proxies qui prennent en charge HTTPS
https_proxies_1 = proxy_list_1[proxy_list_1["Https"]=='yes']
print('\n',https_proxies_1.head())

# Liste de proxies du site : https://spys.one/en/https-ssl-proxy/
print("\nScrapping Proxies 2 : ")
# récupérer la liste des free proxies 
proxy_list_2 = pd.read_csv('/Users/charles-albert/Desktop/Manga Downloader/Proxy Headers/proxies.csv',sep=';')
proxy_list_2['url'] = "http://"+ proxy_list_2['url'].astype(str)

new_https_proxies_1 = https_proxies_1['url'].to_frame(name='url')
new_https_proxies_2 = proxy_list_2['url'].to_frame(name='url')

print('\n',new_https_proxies_1.head(),'\n',new_https_proxies_2.head())

https_proxies_concat = pd.concat([new_https_proxies_1,new_https_proxies_2] , ignore_index=True, axis=0)
https_proxies_concat = https_proxies_concat.reset_index(drop=True)

print(https_proxies_concat.head())

good_proxies = Good_proxies(https_proxies_concat)

### Rotate les User_agents et Proxies
headers = []
# Importation du header de Chrome
with open('/Users/charles-albert/Desktop/Manga Downloader/Proxy Headers/headers.yml') as f_headers:
    browser_headers = yaml.safe_load(f_headers)

# Importation des User-Agent de Chrome
with open('/Users/charles-albert/Desktop/Manga Downloader/UA_Scrapper/User_Agents.yml') as User_Agents:
    User_Agents = yaml.safe_load(User_Agents)

# User_Agents["Chrome"] contient 20 User_agents, On crée donc 20 headers différents stockés dans 'headers'
for i in range(0,19):
    browser_headers["Chrome"]['User-Agent'] = User_Agents["Chrome"][i] 
    headers.append(browser_headers["Chrome"]['User-Agent'])

#==============================================================================================================================

for proxy_url in good_proxies:
        proxy = proxy_url.replace("http://", "")

        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True

        firefox_capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": proxy,
            "sslProxy": proxy
        }

        driver = webdriver.Firefox(capabilities=firefox_capabilities)
        try:
            driver.get("https://httpbin.org/ip")
        except Exception:
            pass