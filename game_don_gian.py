import pygame
import sys
from pygame.locals import *
import math
import random

w = 1000
h = 500

yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
beast_color = (51, 0, 102)

pygame.init()

fps = 120
fpsclock = pygame.time.Clock()
d = pygame.display.set_mode((w, h))
pygame.display.set_caption('Ball vs Beast')


class Beast:
    def __init__(self, x, y):
        # vị trí ban đầu của quái vật
        self.fy = False
        self.fx = False
        self.gameover = False
        self.x = x
        self.y = y

        # tạo surface cho quái vật

        self.surface = pygame.Surface((100, 100), SRCALPHA)
        pygame.draw.line(self.surface, red, (50, 50), (0, 0), 4)
        pygame.draw.line(self.surface, red, (50, 50), (100, 0), 4)
        pygame.draw.circle(self.surface, beast_color, (50, 50), 50)

    def draw(self):
        d.blit(self.surface, (self.x, self.y))

    def update(self, ball_x, ball_y):
        if self.x > ball_x - 25:
            self.x -= 2
        if self.x < ball_x - 25:
            self.x += 2
        if self.y > ball_y - 25:
            self.y -= 2
        if self.y < ball_y - 25:
            self.y += 2

        if self.x < ball_x:
            if ball_x - self.x <= 75:
                if self.y < ball_y:
                    if ball_y - self.y <= 75:
                        self.gameover = True
                elif self.y > ball_y:
                    if self.y - ball_y <= 25:
                        self.gameover = True
        elif self.x > ball_x:
            if self.x - ball_x <= 25:
                if self.y < ball_y:
                    if ball_y - self.y <= 75:
                        self.gameover = True
                elif self.y > ball_y:
                    if self.y - ball_y <= 25:
                        self.gameover = True


class Point:

    def __init__(self):
        self.point = 0
        # vị trí điểm ban đầu được random
        self.x = round(random.randrange(0, w - 50) / 10.0) * 10.0
        self.y = round(random.randrange(0, h - 50) / 10.0) * 10.0

        self.surface = pygame.Surface((50, 50), SRCALPHA)
        pygame.draw.circle(self.surface, yellow, (25, 25), 25)

    def draw(self):
        d.blit(self.surface, (self.x, self.y))

    def update(self, ball_x, ball_y):
        if (math.fabs(self.x - ball_x) <= 25) and (math.fabs(self.y - ball_y) <= 25):
            self.x = round(random.randrange(0, w - 50) / 10.0) * 10.0
            self.y = round(random.randrange(0, h - 50) / 10.0) * 10.0
            self.point += 1


class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        # tạo surface và vẽ hình quả bóng
        self.surface = pygame.Surface((50, 50), SRCALPHA)
        pygame.draw.circle(self.surface, red, (25, 25), 25)

    def draw(self):  # vẽ qủa bóng
        d.blit(self.surface, (self.x, self.y))
    def update(self, moveLeft, moveRight, moveUP, moveDOWN):  # Hàm dùng để thay đổi vị trí quả bóng
        if moveLeft == True:
            self.x -= 5
        if moveRight == True:
            self.x += 5

        if self.x + 50 > w:
            self.x = w - 50
        if self.x < 0:
            self.x = 0

        if moveUP == True:
            self.y -= 5
        if moveDOWN == True:
            self.y += 5

        if self.y + 50 > h:
            self.y = h - 50
        if self.y < 0:
            self.y = 0


class Bang:
    def __init__(self, point, size_font):
        self.f = pygame.font.SysFont('consolas', size_font)
        self.surface = self.f.render(point, True, white, SRCALPHA)

    def draw(self, x, y):
        d.blit(self.surface, (x, y))


ball = Ball()
beast1 = Beast(900, 400)
coin1 = Point()

moveLeft = False
moveRight = False
moveUP = False
moveDOWN = False
start = False
continue_game = False
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                moveLeft = True
            if event.key == K_RIGHT:
                moveRight = True
            if event.key == K_UP:
                moveUP = True
            if event.key == K_DOWN:
                moveDOWN = True
            if event.key == K_s:
                start = True
            if beast1.gameover:
                if event.key == K_y:
                    continue_game = True
                    if continue_game:
                        ball = Ball()
                        beast1 = Beast(900, 400)
                        coin1 = Point()
                        moveLeft = False
                        moveRight = False
                        moveUP = False
                        moveDOWN = False
                        start = False
                        continue_game = False

                if event.key == K_n:
                    pygame.quit()
                    sys.exit()
        if event.type == KEYUP:
            if event.key == K_LEFT:
                moveLeft = False
            if event.key == K_RIGHT:
                moveRight = False
            if event.key == K_UP:
                moveUP = False
            if event.key == K_DOWN:
                moveDOWN = False

    if coin1.point % 10 == 0 and coin1.point != 0:
        d.fill(red)
        Warning_speed = Bang('Warning!!!', 30, black)
        Warning_speed.draw(60, 20)
        beast1.speed = 3


    d.fill(black)

    ball.draw()

    ball_x = ball.x
    ball_y = ball.y

    coin1.draw()
    coin1.update(ball_x, ball_y)

    beast1.draw()

    if start:
        beast1.update(ball_x, ball_y)

    p = str(coin1.point)

    bdiem1 = Bang(p, 30)
    bdiem1.draw(20, 20)
    if not beast1.gameover:

        if start:
            ball.update(moveLeft, moveRight, moveUP, moveDOWN)

    else:
        thongbao = Bang('GAME OVER NHẤN Y ĐỂ CHƠI LẠI N ĐỂ THOÁT GAME', 20)
        thongbao.draw(w / 4, h / 3)
    if not start:
        thongbao = Bang('NHẤN S ĐỂ CHƠI', 50)
        thongbao.draw(w / 3, h / 3)

    pygame.display.update()
    fpsclock.tick(fps)