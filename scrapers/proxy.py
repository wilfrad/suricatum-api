import time
import concurrent.futures
import requests
from colorama import Fore
from bs4 import BeautifulSoup

HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}

PROXIES = []

URL_TARGET = 'https://www.google.com/'

def proxy_request(url, method=None):

  req = requests.get(url, headers=HEADERS, timeout=10)
  return req

  for proxy in PROXIES:

    try:
      proxies = {"http": proxy, "https": proxy}

      print(f"{Fore.YELLOW} Proxy currently being used: {proxy} for url: {url} {Fore.WHITE}")
      req = requests.get(url, headers=HEADERS, timeout=10)

      if req.status_code == 200:
        return req

      print(f"{Fore.RED} Proxy: {proxy} not response {Fore.WHITE}")

    except Exception as err:
      print(err)

  print(f'{Fore.RED} No valid proxies {Fore.WHITE}')
  return None

def filter_proxies(proxies):

    valid_proxies = {}
    promises = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
      for proxy in proxies:
        promises.append(executor.submit(_check_proxy, proxy, URL_TARGET))

    for promise in concurrent.futures.as_completed(promises):
        result = promise.result()
        if result["res"] == 200:
          valid_proxies[result["proxy"]] = result["time"]

    print(Fore.WHITE)
    
    if len(valid_proxies) > 0:
      print('valid proxies---------------------------')
      for proxy, time in valid_proxies.items():
        print(f' - {proxy}: {time:.2f}s')

    return valid_proxies

def _check_proxy(proxy, url):

  response = {
      "proxy": proxy,
      "time": None,
      "res": None,
  }

  try:
    proxies = {
        "http": proxy,
        "https": proxy,
    }

    init = time.time()

    req = requests.get(url, headers=HEADERS, proxies=proxies, timeout=10)

    response["time"] = time.time() - init
    response["res"] = req.status_code

  except Exception as err:
    pass

  return response

def get():

    proxies = []

    results = _get_free_proxy_list()
    print(f' {len(results["list"])} {results["origen"]}')
    proxies.extend(results["list"])

    results = _get_proxyscrape()
    print(f' {len(results["list"])} {results["origen"]}')
    proxies.extend(results["list"])

    proxies = list(set(proxies))

    return proxies

def _remove_proxy():

  print(Fore.RED)

  try:
    PROXIES.remove(proxy)
    print(f'proxy "{proxy}" is removed')
  except Exception:
    print(f'proxy "{proxy}" is not found')

  print(Fore.WHITE)

def _get_proxyscrape():

  req = requests.get("https://api.proxyscrape.com/proxytable.php?nf=true&country=all", headers=HEADERS, timeout=10)
  data = req.json()

  proxies = []
  for k,v in data ["http"].items():
    if v["anonymity"] == 3:
      proxies.append(k)

  for k,v in data ["socks5"].items():
    if v["anonymity"] == 3:
      proxies.append(k)

  return {
    "origen": "Proxy Scrape",
    "list": proxies
  }

def _get_free_proxy_list():

  req = requests.get("https://free-proxy-list.net/", headers=HEADERS, timeout=10)

  soup = BeautifulSoup(req.text, "html.parser")

  rows = soup.find("tbody").find_all("tr")

  proxies = []
  for row in rows:
    field = row.find_all("td")

    proxy_ip = field[0].text
    proxy_port = field[1].text

    proxy_type = field[4].text
    if proxy_type == "elite proxy":
      proxy = f"{proxy_ip}:{proxy_port}"
      proxies.append(proxy)

  return {
    "origen": "Free Proxy List",
    "list": proxies
  }

def evaluate_proxies():

  LASTED_PROXIES = None
  with open("app/scrapers/data/proxy_list.txt", "r", encoding='utf-8') as file:
    LASTED_PROXIES = file.readlines()
    file.close()

  global PROXIES
  if len(LASTED_PROXIES) > 2:
    proxies = []
    for item in LASTED_PROXIES:
      proxies.append(item.strip())

    print(f'{Fore.GREEN} Loaded lasted proxies {Fore.WHITE}')
    PROXIES = proxies
  else:
    proxies = get()

    init = time.time()
    valid_proxies = filter_proxies(proxies)
    if valid_proxies:
      timeout = int(time.time() - init)
      print(f'valid proxies....: {len(valid_proxies)}')
      print(f'total time.......: {timeout}')

      with open("app/scrapers/data/proxy_list.txt", "w", encoding='utf-8') as file:
        file.write("\n".join(valid_proxies))
        file.close()

      PROXIES = list(valid_proxies)
    else:
      PROXIES = []
      print(f'{Fore.RED} Finish evaluation. No valid proxies {Fore.WHITE}')