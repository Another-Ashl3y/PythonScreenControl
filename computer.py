import socket
from PIL import ImageGrab
import time
import tkinter as tk
root = tk.Tk()

monitor_res = (root.winfo_screenwidth(), root.winfo_screenheight())
print(monitor_res)

server = "127.0.0.1" #input("Ip > ")
port = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
s.sendall("hello world".encode("utf-8"))


def encode_window():
    data = ImageGrab.grab().load()
    message = "?m"
    for y in range(0, 2304, 10):
        for x in range(0, 4096, 10):
            colour = int(sum(data[x,y])/3)
            # if colour > 255/2:
            #     message+="255,"
            # else:
            #     message+="000,"
            message += f"{colour},"
        message+="\n"
    print(len(message))
    with open("screen.txt","w") as f:
        f.write(message)
    return message

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    s.sendall(encode_window().encode("utf-8"))
    print("update sent")
    time.sleep(1)