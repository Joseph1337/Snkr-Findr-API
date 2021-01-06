import requests
import random
from bs4 import BeautifulSoup as bs

def get_proxy_list():
    url = "https://sslproxies.org/"
    # get the HTTP response and construct soup object
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies

def get_random_proxy():
    # rand_proxy = random.choice(get_proxy_list())
    for i in range(0, 100):
        try:
            # print("working")
            proxy = random.choice(get_proxy_list())
            response = requests.get("http://icanhazip.com/", proxies={'http': "http://" + proxy, 'https': "https://" + proxy}, timeout=1)
        except:
            # print("searching for new proxy")
            continue
        break

    else:
        print("No proxy found")
        return

    return proxy


def get_session(proxies):
    # construct an HTTP session
    session = requests.Session()
    # choose one random proxy
    proxy = random.choice(proxies)
    session.proxies = {"http": "http://" + proxy, "https": "https://" + proxy}
    return session


# if __name__ == "__main__":
#     print(get_random_proxy())
    # print(get_proxy_list())
    # for i in range(100):
    #     s = get_session(get_proxy_list())
    #     try:
    #         response = requests.get("http://icanhazip.com", proxies={'http': "http://" + get_random_proxy(), 'https': "https://" + get_random_proxy()}, timeout=1)
    #         print("Request page with IP:", response.text.strip())
    #         print(response.status_code)
    #     except Exception as e:
    #         print(e)
    #         continue
    # else:
    #     print("Failed")

