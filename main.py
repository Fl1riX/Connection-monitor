import psutil, tkinter as tk, requests, random, threading
from proxies import parse
from proxy import free_proxies
from fake_useragent import UserAgent

class Main_win:
    
    def __init__(self) -> None:
        self.connections = psutil.net_connections(kind="inet")
        self.cons = []
        
        self.win = tk.Tk()
        self.win.title("Connection Monitor")
        self.win.geometry("800x500+230+200")
        self.win.resizable(1, 1)

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


        self.refresh_bt = tk.Button(self.bt_frame, text="Refresh", command=self.get_ips)
        self.refresh_bt.grid(row=1, column=0, pady=10)
        
        self.kill_all_bt = tk.Button(self.bt_frame, text="kill all", command=self.kill_all_connections)
        self.kill_all_bt.grid(row=1, column=1, pady=10, padx=5)

        self.nc_bt = tk.Button(self.bt_frame, text="netcards", command=Netcards_inf)
        self.nc_bt.grid(row=1, column=2, pady=10)


        self.win.grid_rowconfigure(0, weight=1)
        self.win.grid_columnconfigure(0, weight=1)
        
        self.get_ips()

        self.win.mainloop()

    def get_ips(self):
        self.cons.clear()
        self.connections = psutil.net_connections() 
        for conn in self.connections:
            if conn.status == "ESTABLISHED":
                if conn.raddr:
                    self.cons.append(f"Remote: {conn.raddr.ip}:{conn.raddr.port} | Local: {conn.laddr.ip}:{conn.laddr.port}")
        self.cons_var.set(self.cons)
        
    def kill_all_connections(self):
        for conn in self.connections:
            if conn.pid:  
                pid = conn.pid
                process = psutil.Process(pid)
                process.terminate()

    def show_info_window(self, event):
        header = self.listbox.curselection()
        if header:
            selected_ip = self.listbox.get(header)
            th1 = threading.Thread(target=InfoWindow, args=(selected_ip, self.connections, )) 
            th1.start()

class InfoWindow:
    
    def __init__(self, ip, conns):
        self.wind = tk.Toplevel()
        self.wind.geometry('500x255+1030+300')
        self.wind.resizable(0, 0)
        
        sp1 = ip.split('|')
        sp2 = sp1[0].split("Remote: ")
        
        self.wind.title(sp2[1])
        
        self.kill_connection_bt = tk.Button(self.wind, text="Kill connection", command=lambda: self.kill_connection(conns))
        self.kill_connection_bt.grid(column=0, row=1)
        
        self.ip_port = sp2[1].split(":")
        
        self.ip_inf = tk.Text(self.wind, height=10, width=62)
        self.ip_inf.grid(column=0, row=0)
        
        self.parse_ip_inf(self.ip_port[0])
        
    def parse_ip_inf(self, ip):
        try:
            parse()

            headers = {"User-Agent" : f"{UserAgent().random}"}
            proxy = {"http": random.choice(free_proxies)}
            response = requests.get(f"https://ipinfo.io/{ip}/json", proxies=proxy, headers=headers)

            if response.status_code == 200:
                result = response.text
                self.ip_inf.insert("1.0", f"ipinfo: {result}\n")
        except Exception as e:
            print(f"ERROR!!!: {e}")
    
    def kill_connection(self, connections):
        try:
            for conn in connections:
                if conn.raddr and conn.raddr.ip == self.ip_port[0]:  
                    pid = conn.pid
                    if pid:
                        process = psutil.Process(pid)
                        process.terminate()

            print(f"IP: {self.ip_port[0]} was killed")
        except Exception as e:
            print(e)
        
class Netcards_inf():
    def __init__(self) -> None:
        self.net_card_win = tk.Toplevel()
        self.net_card_win.geometry("700x450")
        self.net_card_win.resizable(0, 0)
        self.net_card_win.title("Netcards info")
        
        
        self.info_text = tk.Text(self.net_card_win, heigh=27, width=86)
        self.info_text.grid(column=0, row=0)
        self.info_text.insert("1.0", psutil.net_if_addrs())
            
if __name__ == "__main__":
    Main_win()
