import socket

server = "127.0.0.1" #input("Ip > ")
port = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
s.sendall("hello world".encode("utf-8"))
while True:
    data = s.recv(1024)
    print(data.decode("utf-8"))
    s.sendall(input("> ").encode("utf-8"))

