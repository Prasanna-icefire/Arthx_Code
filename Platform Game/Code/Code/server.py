import pygame
import socket
import threading
import atexit


def handel_exit():
    print("bye")
    s.close()


def recive_data():
    global data
    while True:
        data = conn.recv(1024).decode()
        print(data)
        draw_o(int(data[0]), int(data[2]))




def connection():
    global conn, addr, conect
    s.listen(5)
    print("Listening...")
    conn, addr = s.accept()
    print("Connected to", addr)
    conect = True
    recive_data()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = ''
PORT = 12345
s.bind((HOST, PORT))
conect = False
thread = threading.Thread(target=connection)
thread.start()

pygame.init()
size = (600, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("TicTacToe")


def draw_x(x, y):
    pygame.draw.line(screen, white, (50 + 200 * x, 50 + 200 * y), (150 + 200 * x, 150 + 200 * y))
    pygame.draw.line(screen, white, (150 + 200 * x, 50 + 200 * y), (50 + 200 * x, 150 + 200 * y))


def draw_o(x, y):
    pygame.draw.circle(screen, white, (100 + 200 * x, 100 + 200 * y), 75, 5)


black = (0, 0, 0)
white = (255, 255, 255)
Run = True
screen.fill(black)
while Run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and conect:
            x, y = event.pos
            draw_x(x // 200, y // 200)
            send_data = str(x // 200) + "," + str(y // 200)
            conn.send(send_data.encode())

    pygame.draw.line(screen, white, (200, 0), (200, 600))
    pygame.draw.line(screen, white, (400, 0), (400, 600))
    pygame.draw.line(screen, white, (0, 200), (600, 200))
    pygame.draw.line(screen, white, (0, 400), (600, 400))

    pygame.display.update()
    atexit.register(handel_exit)
