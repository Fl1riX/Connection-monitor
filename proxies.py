from bs4 import BeautifulSoup
import requests
import logging
import os

logging.basicConfig(level=logging.INFO, filename="monitor_logs.log", filemode="a", encoding="utf-8")

def parse():
    link = "https://free-proxy-list.net/"
    response = requests.get(url=link)

    if response.status_code == 200:
        bsd = BeautifulSoup(response.text, "html.parser")
        proxy_data = []

        for row in bsd.select("table.table tbody tr"):
            columns = row.find_all("td")

            if len(columns) >= 8:
                ip = columns[0].get_text()
                port = columns[1].get_text()
                htt = columns[6].get_text()
                
                if htt.lower() == "no":
                    proxy_data.append(f"{ip}:{port}")

        with open('proxy.py', 'w', encoding="utf-8") as file:
            file.write(f"free_proxies = {str(proxy_data)}")

        logging.info(f"Парсер успешно собрал {len(proxy_data)} прокси и записал в proxy.py")

    else:
        logging.error(f"Ошибка парсинга прокси. Код ответа: {response.status_code}")
