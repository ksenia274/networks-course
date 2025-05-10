import socket
import threading
import tkinter as tk
from tkinter import messagebox
import random
import time

def send_packets(ip, port, count, protocol):
    lost = 0
    data = bytes(random.getrandbits(8) for _ in range(1024))
    start_time = time.time()

    if protocol == "TCP":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, int(port)))
        for _ in range(count):
            try:
                sock.sendall(data)
            except:
                lost += 1
        sock.close()
    else:  # UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for _ in range(count):
            try:
                sock.sendto(data, (ip, int(port)))
            except:
                lost += 1
        sock.close()

    duration = time.time() - start_time
    speed = (count - lost) * 1024 / duration
    messagebox.showinfo("Результат", f"Скорость передачи: {speed:.2f} B/s\nПотеряно пакетов: {lost} из {count}")

def start_client():
    ip = entry_ip.get()
    port = entry_port.get()
    count = int(entry_count.get())
    protocol = var.get()
    threading.Thread(target=send_packets, args=(ip, port, count, protocol)).start()

root = tk.Tk()
root.title("Клиент TCP/UDP")

tk.Label(root, text="IP").grid(row=0, column=0)
entry_ip = tk.Entry(root)
entry_ip.insert(0, "127.0.0.1")
entry_ip.grid(row=0, column=1)

tk.Label(root, text="Порт").grid(row=1, column=0)
entry_port = tk.Entry(root)
entry_port.insert(0, "8080")
entry_port.grid(row=1, column=1)

tk.Label(root, text="Кол-во пакетов").grid(row=2, column=0)
entry_count = tk.Entry(root)
entry_count.insert(0, "5")
entry_count.grid(row=2, column=1)

var = tk.StringVar(value="TCP")
tk.Radiobutton(root, text="TCP", variable=var, value="TCP").grid(row=3, column=0)
tk.Radiobutton(root, text="UDP", variable=var, value="UDP").grid(row=3, column=1)

tk.Button(root, text="Отправить", command=start_client).grid(row=4, columnspan=2)

root.mainloop()