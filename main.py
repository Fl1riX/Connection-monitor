import psutil
import tkinter as tk
import requests
import random
import threading
import logging
from proxies import parse
from proxy import free_proxies
from uas import UAS 

# Настройка логирования
logging.basicConfig(
    filename="monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class ConnectionMonitor:
    """Главное окно программы для мониторинга соединений."""

    def __init__(self) -> None:
        self.win = tk.Tk()
        self.win.title("Connection Monitor")
        self.win.geometry("800x500+230+200")
        self.win.resizable(0, 0)

        self.connections = []
        self.cons_var = tk.StringVar(value=self.connections)

        self.create_widgets()
        self.update_connections()

        logging.info("Запущен Connection Monitor")
        self.win.mainloop()

    def create_widgets(self):
        """Создаёт интерфейсные элементы."""

        # Фрейм для списка соединений
        self.frame = tk.Frame(self.win)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Список соединений
        self.listbox = tk.Listbox(self.frame, listvariable=self.cons_var, height=25, width=129)
        self.listbox.grid(row=0, column=0, sticky="nsew")
        self.listbox.bind("<Double-Button-1>", self.show_info_window)

        # Скроллбар для списка
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Фрейм с кнопками
        self.bt_frame = tk.Frame(self.win)
        self.bt_frame.grid(row=1, column=0, pady=10)

        # Кнопки управления
        tk.Button(self.bt_frame, text="Refresh", command=self.update_connections).grid(row=1, column=0, pady=10)
        tk.Button(self.bt_frame, text="Kill all", command=self.kill_all_connections).grid(row=1, column=1, pady=10, padx=5)
        tk.Button(self.bt_frame, text="Netcards", command=NetcardsInfo).grid(row=1, column=2, pady=10)

        self.win.grid_rowconfigure(0, weight=1)
        self.win.grid_columnconfigure(0, weight=1)

    def update_connections(self):
        """Обновляет список активных соединений."""
        self.connections.clear()
        for conn in psutil.net_connections(kind="inet"):
            if conn.status == "ESTABLISHED" and conn.raddr:
                self.connections.append(f"Remote: {conn.raddr.ip}:{conn.raddr.port} | Local: {conn.laddr.ip}:{conn.laddr.port}")
        self.cons_var.set(self.connections)
        logging.info(f"Обновлено {len(self.connections)} соединений")

    def kill_all_connections(self):
        """Прерывает все активные соединения."""
        for conn in psutil.net_connections(kind="inet"):
            if conn.pid:
                try:
                    psutil.Process(conn.pid).terminate()
                    logging.info(f"Процесс {conn.pid} завершён")
                except Exception as e:
                    logging.error(f"Ошибка при завершении процесса {conn.pid}: {e}")

    def show_info_window(self, event):
        """Открывает окно с информацией о соединении."""
        selected = self.listbox.curselection()
        if selected:
            ip_info = self.listbox.get(selected)
            threading.Thread(target=InfoWindow, args=(ip_info,)).start()


class InfoWindow:
    """Окно информации о соединении и удалённом IP."""

    def __init__(self, ip_info):
        self.wind = tk.Toplevel()
        self.wind.geometry("500x255+1030+300")
        self.wind.resizable(0, 0)

        remote_info = ip_info.split("|")[0].replace("Remote: ", "")
        self.ip, self.port = remote_info.split(":")
        self.wind.title(self.ip)

        tk.Button(self.wind, text="Kill connection", command=self.kill_connection).grid(column=0, row=1)

        self.ip_info_text = tk.Text(self.wind, height=10, width=62)
        self.ip_info_text.grid(column=0, row=0)

        self.get_ip_info()

    def get_ip_info(self):
        """Запрашивает информацию об IP через API."""
        try:
            parse()
            headers = {"User-Agent": random.choice(UAS)}
            proxy = {"http": random.choice(free_proxies)}

            response = requests.get(f"https://ipinfo.io/{self.ip}/json", proxies=proxy, headers=headers)

            if response.status_code == 200:
                self.ip_info_text.insert("1.0", f"IP Info: {response.text}\n")
                logging.info(f"Получена информация об IP {self.ip}")
            else:
                logging.warning(f"Ошибка при запросе IP {self.ip}: {response.status_code}")

        except Exception as e:
            logging.error(f"Ошибка при получении информации об IP {self.ip}: {e}")

    def kill_connection(self):
        """Завершает соединение с указанным IP."""
        try:
            for conn in psutil.net_connections(kind="inet"):
                if conn.raddr and conn.raddr.ip == self.ip:
                    if conn.pid:
                        psutil.Process(conn.pid).terminate()
                        logging.info(f"Соединение с {self.ip} завершено (PID {conn.pid})")
                        break
        except Exception as e:
            logging.error(f"Ошибка при завершении соединения с {self.ip}: {e}")


class NetcardsInfo:
    """Окно с информацией о сетевых интерфейсах."""

    def __init__(self):
        self.net_card_win = tk.Toplevel()
        self.net_card_win.geometry("700x450")
        self.net_card_win.resizable(0, 0)
        self.net_card_win.title("Netcards Info")

        self.info_text = tk.Text(self.net_card_win, height=27, width=86)
        self.info_text.grid(column=0, row=0)

        self.info_text.insert("1.0", str(psutil.net_if_addrs()))
        logging.info("Открыто окно информации о сетевых интерфейсах")


if __name__ == "__main__":
    ConnectionMonitor()
