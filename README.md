Here's a well-formatted `README.md` in English with some special characters for better readability:

---

# 💻 **Connection Monitor** 🔍

**Connection Monitor** is a Python-based program designed to monitor active network connections on your machine. It uses the `psutil` library to retrieve system information and `tkinter` for the graphical user interface (GUI). The app allows you to monitor, kill, and get detailed information about your network connections and network cards.

---

## 🛠️ **Installation** 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/Fl1riX/-onnection-Monitor.git
   cd -onnection-Monitor
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the program:
   ```bash
   python main.py
   ```

---

## 📦 **Dependencies** 📦

The program requires the following Python libraries:

- **psutil** — For working with network connections and process information.
- **socket** — For network operations.
- **tkinter** — For creating the GUI.
- **requests** — For making HTTP requests (e.g., to `ipinfo.io`).
- **random** — For selecting random proxy.
- **fake_useragent** — For generating random `User-Agent` headers.
- **threading** — To create threads, ensuring the UI remains responsive.

---

## 📁 **Project Files** 📁

- **main.py** — The main program file.
- **proxies.py** — The proxy handler script.
- **proxy.py** — Contains a list of free proxies.
- **requirements.txt** — A list of dependencies for installation via `pip`.
- **.gitignore** — Git ignore file to exclude unnecessary files from the repository.

---

## 📝 **How to Use** 📝

1. **Launch the Program**: Run the program using the command `python main.py`.
2. **Monitor Active Connections**: View a list of active network connections.
3. **Use the Control Buttons**:
   - **Refresh**: Refresh the list of active connections.
   - **Kill All**: Terminate all active connections.
   - **Netcards**: Open a window with information about your network cards.
4. **View Detailed Connection Info**: Double-click on any connection in the list to view detailed information about it.

---

## 🎥 **Example Usage** 🎥

- The main window of the program displays the list of active connections.
- The buttons are located at the bottom, allowing you to refresh the list, terminate connections, or check network card details.

---

## ⚠️ **Notes** ⚠️

1. An active internet connection is required for fetching IP details.
2. You might need administrator privileges to terminate network-related processes.

---

## 👨‍💻 **Author** 👩‍💻

[Fl1riX](https://github.com/Fl1riX)  
This project is created for monitoring network connections and retrieving network-related information.

---

Feel free to modify the design or make improvements as necessary. This version includes a clean layout and special characters for better readability! 😊