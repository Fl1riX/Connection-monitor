from bs4 import BeautifulSoup 
import requests

link = "https://free-proxy-list.net/" 
response = requests.get(url=link) 

def parse():
    if response.status_code == 200: 
        bsd = BeautifulSoup(response.text, "html.parser") 
        proxy_data = [] 
        
        for row in bsd.select("table.table tbody tr"):
            columns = row.find_all("td")
            
            if len(columns) >= 8: 
                ip = columns[0].get_text()
                port = columns[1].get_text()
                htt = columns[6].get_text()
                if htt == "no":
                    proxy_data.append(f"{ip}:{port}")
                else:
                    pass

        with open('proxy.py', 'w', encoding="utf-8") as file: 
            file.write(f"free_proxies = {str(proxy_data)}")
    else:
        print("Error:", response.status_code)
        
#if __name__ == "__main__":
#    parse()