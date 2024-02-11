from uu import Error
import pygame
import os
import random
import time
import socket
from _thread import *

server = "127.0.0.1" # input("Ip: ")
port = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

screen_width = int(4096/10)
screen_height = int(2304/10)
screen = [[((x/screen_width)*(y/screen_height))*255 for x in range(screen_width)] for y in range(screen_height)]
updated = False

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def threaded_client(conn):
    global updated
    conn.send(str.encode("Connected"))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("Closing Server")
                return
        try:
            data = conn.recv(320000)
            reply = data.decode("utf-8")
            if len(reply) >= 4:
                print("Monitor Update")
                if reply[0:2] == "?m":
                    window = reply[2:].split(",\n")
                    for y, i in enumerate(window):
                        for x, j in enumerate(i.split(",")):
                            if j:
                                if y < len(screen):
                                    if x < len(screen[y]):
                                        screen[y][x] = int(j)
                                    else:
                                        break
                                else:
                                    break

                    # y = 0
                    # for i in window:
                    #     x.clear()
                    #     for j in i.split(","):
                    #         if j:
                    #             x.append(int(j))
                    #     time.sleep(0.1)
                    #     y += 1




                    # for i in range(int(screen_height)):
                    #     x.clear()
                    #     y = i
                    #     for j in range(int(screen_width)):
                    #         print("line update")
                    #         # print(j%(screen_width/5),i//(screen_height/5))
                    #         index = int((i*(screen_width/5))+j)
                    #         # print(index, j, i)
                    #         try:
                    #             if window[int((i*(screen_width/5))+j)]:
                    #                 if index < len(window):
                    #                     x.append(int(window[index]))
                    #         except IndexError as e:
                    #             print(index, "too big for", len(window))
                    #             break
                    #     time.sleep(0.2)
                    updated = False
            if not data:
                print("Disconnected", conn)
                break
            else:
                # print("Received: ", reply)
                pass
            
            conn.sendall(str.encode(reply))
        except Error as e: 
            print(e)
            break

    print("Lost connection")
    conn.close()

def update_pygame():
    global updated
    width, height = screen_width, screen_height
    win = pygame.display.set_mode((width, height))
    while True:
        # print("Window updated")
        if not updated:
            # win.fill((0,0,0))
            updated = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        for x in range(screen_width):
            for y in range(screen_height):
                c = int(screen[y][x])
                pygame.draw.rect(win, (c,c,c), (x,y,1,1))


        # for x_pos, c in enumerate(x):
        #     pygame.draw.rect(win, (c,c,c), (x_pos,y,1,1))

        pygame.display.update()

def main():
    start_new_thread(update_pygame, ())
    while True:
        conn, addr = s.accept()
        print("Connected to: ", addr)
        start_new_thread(threaded_client, (conn, ))
        pygame.display.update()

if __name__=="__main__":           
    main()
