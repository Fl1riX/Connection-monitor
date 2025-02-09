import psutil
import tkinter as tk
import requests
import random
import threading
import logging
import os
import importlib.util
from proxies import parse
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO, filename="monitor_logs.log", filemode="a", encoding="utf-8")

if not os.path.exists("proxy.py"):
    logging.info("Файл proxy.py отсутствует, выполняется парсинг прокси...")
    parse()
else:
    logging.info("Парсинг прокси")
    parse()

spec = importlib.util.spec_from_file_location("proxy", "proxy.py")
proxy_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proxy_module)
free_proxies = proxy_module.free_proxies

class ConnectionMonitor:
    @staticmethod
    def get_active_connections():
        connections = []
        for conn in psutil.net_connections(kind="inet"):
            if conn.status == "ESTABLISHED" and conn.raddr:
                connections.append(conn)
        logging.info(f"Получено {len(connections)} активных соединений")
        return connections

    @staticmethod
    def kill_connection(ip):
        for conn in psutil.net_connections(kind="inet"):
            if conn.raddr and conn.raddr.ip == ip:
                try:
                    if conn.pid:
                        process = psutil.Process(conn.pid)
                        process.terminate()
                        logging.info(f"Соединение с {ip} завершено")
                except Exception as e:
                    logging.error(f"Ошибка при завершении соединения {ip}: {e}")

    @staticmethod
    def kill_all_connections():
        for conn in psutil.net_connections(kind="inet"):
            try:
                if conn.pid:
                    process = psutil.Process(conn.pid)
                    process.terminate()
            except Exception as e:
                logging.error(f"Ошибка при завершении процесса: {e}")

class MainWin:
    def __init__(self):
        self.connections = ConnectionMonitor.get_active_connections()
        self.cons = []

        self.win = tk.Tk()
        self.win.title("Connection Monitor")
        self.win.geometry("800x500+230+200")
        self.win.resizable(False, False)

        self.frame = tk.Frame(self.win)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.bt_frame = tk.Frame(self.win)
        self.bt_frame.grid(row=1, column=0, pady=10)

        self.cons_var = tk.StringVar(value=self.cons)
        self.listbox = tk.Listbox(self.frame, listvariable=self.cons_var, height=25, width=129)
        self.listbox.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="wnse")

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.bind("<Double-Button-1>", self.show_info_window)

        self.refresh_bt = tk.Button(self.bt_frame, text="Refresh", command=self.update_connections)
        self.refresh_bt.grid(row=1, column=0, pady=10)

        self.kill_all_bt = tk.Button(self.bt_frame, text="Kill All", command=ConnectionMonitor.kill_all_connections)
        self.kill_all_bt.grid(row=1, column=1, pady=10, padx=5)

        self.nc_bt = tk.Button(self.bt_frame, text="Netcards", command=self.open_netcards_info)
        self.nc_bt.grid(row=1, column=2, pady=10)

        self.win.grid_rowconfigure(0, weight=1)
        self.win.grid_columnconfigure(0, weight=1)

        self.update_connections()
        self.win.mainloop()

    def update_connections(self):
        self.cons.clear()
        self.connections = ConnectionMonitor.get_active_connections()
        for conn in self.connections:
            self.cons.append(f"Remote: {conn.raddr.ip}:{conn.raddr.port} | Local: {conn.laddr.ip}:{conn.laddr.port}")
        self.cons_var.set(self.cons)
        logging.info("Список соединений обновлен")

    def show_info_window(self, event):
        selection = self.listbox.curselection()
        if selection:
            selected_conn = self.listbox.get(selection)
            threading.Thread(target=InfoWindow, args=(selected_conn,)).start()

    def open_netcards_info(self):
        NetcardsInfo()

class InfoWindow:
    def __init__(self, connection_str):
        self.wind = tk.Toplevel()
        self.wind.geometry('500x255+1030+300')
        self.wind.resizable(False, False)

        ip = connection_str.split("|")[0].split("Remote: ")[1].split(":")[0]
        self.wind.title(ip)

        self.kill_connection_bt = tk.Button(self.wind, text="Kill Connection",
                                            command=lambda: ConnectionMonitor.kill_connection(ip))
        self.kill_connection_bt.grid(column=0, row=1)

        self.ip_inf = tk.Text(self.wind, height=10, width=62)
        self.ip_inf.grid(column=0, row=0)

        self.parse_ip_info(ip)

    def parse_ip_info(self, ip):
        try:
            headers = {"User-Agent": UserAgent().random}
            proxy = {"http": random.choice(free_proxies)}
            response = requests.get(f"https://ipinfo.io/{ip}/json", proxies=proxy, headers=headers)

            if response.status_code == 200:
                result = response.text
                self.ip_inf.insert("1.0", f"IP Info: {result}\n")
                logging.info(f"Информация по IP {ip} успешно получена")
        except Exception as e:
            logging.error(f"Ошибка при запросе к IPInfo: {e}")

class NetcardsInfo:
    def __init__(self):
        self.net_card_win = tk.Toplevel()
        self.net_card_win.geometry("700x450")
        self.net_card_win.resizable(False, False)
        self.net_card_win.title("Netcards Info")

        self.info_text = tk.Text(self.net_card_win, height=27, width=86)
        self.info_text.grid(column=0, row=0)
        self.info_text.insert("1.0", str(psutil.net_if_addrs()))
        logging.info("Открыто окно информации о сетевых картах")

if __name__ == "__main__":
    logging.info("Запуск Connection Monitor")
    MainWin()
