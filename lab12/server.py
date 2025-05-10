import socket
import threading
import tkinter as tk

received_packets = 0

def tcp_server(ip, port):
    global received_packets
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    conn, _ = server.accept()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        received_packets += 1
    conn.close()

def udp_server(ip, port):
    global received_packets
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((ip, port))
    while True:
        data, _ = server.recvfrom(1024)
        if data:
            received_packets += 1

def start_server():
    global received_packets
    received_packets = 0
    ip = entry_ip.get()
    port = int(entry_port.get())
    protocol = var.get()

    if protocol == "TCP":
        threading.Thread(target=tcp_server, args=(ip, port), daemon=True).start()
    else:
        threading.Thread(target=udp_server, args=(ip, port), daemon=True).start()

    update_label()

def update_label():
    label_result.config(text=f"Получено пакетов: {received_packets}")
    root.after(1000, update_label)

root = tk.Tk()
root.title("Сервер TCP/UDP")

tk.Label(root, text="IP").grid(row=0, column=0)
entry_ip = tk.Entry(root)
entry_ip.insert(0, "127.0.0.1")
entry_ip.grid(row=0, column=1)

tk.Label(root, text="Порт").grid(row=1, column=0)
entry_port = tk.Entry(root)
entry_port.insert(0, "8080")
entry_port.grid(row=1, column=1)

var = tk.StringVar(value="TCP")
tk.Radiobutton(root, text="TCP", variable=var, value="TCP").grid(row=2, column=0)
tk.Radiobutton(root, text="UDP", variable=var, value="UDP").grid(row=2, column=1)

tk.Button(root, text="Запустить", command=start_server).grid(row=3, columnspan=2)
label_result = tk.Label(root, text="Получено пакетов: 0")
label_result.grid(row=4, columnspan=2)

root.mainloop()