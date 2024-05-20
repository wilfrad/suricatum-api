import time
from scrapers.proxy import get_all, filter_proxies

init = time.time()
proxies = get_all()
valid_proxies = filter_proxies(proxies)

if valid_proxies:
    timeout = int(time.time() - init)
    print(f'valid proxies....: {len(valid_proxies)}')
    print(f'total time.......: {timeout}')
    print(f'time by proxy....: {timeout / len(valid_proxies):.2f}')

    with open("app/scrapers/data/proxy_list.txt", "w", encoding='utf-8') as file:
        file.write("\n".join(valid_proxies))
else:
    print('no valid proxies')