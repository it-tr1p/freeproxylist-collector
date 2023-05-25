import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
}


# TODO: Add try / except

def collect_free_proxylist(headers: dict):
    url = "https://freeproxylist.ru/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    # Нахождение кол-ва страниц
    all_pages = soup.find_all("li", class_="page-item")
    last_page = int(all_pages[-1].text.strip())

    # Пробег по каждой странице
    for page in range(1, last_page + 1):
        logging.info(f"Обработка страницы #{page}")
        url = f"https://freeproxylist.ru/proxy-list?page={page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        # Находим таблицу с ip
        all_proxy_table = soup.find("tbody", class_="table-proxy-list")
        all_tr = all_proxy_table.find_all("tr")

        # Достаем ip и port
        for line in all_tr:
            ip = line.find("th")
            port = ip.findNext()

            ip = ip.text.strip()
            port = port.text.strip()
            result = f"{ip}:{port}"

            # Сохраняем ip:port
            with open("proxy_list.txt", "a", encoding="utf-8") as file:
                file.write(result + "\n")


if __name__ == "__main__":
    collect_free_proxylist(headers=headers)
