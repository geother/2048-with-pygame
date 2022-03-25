import random
import pygame
import pygame.freetype
from pygame.locals import *

pygame.init()

screenInfo = pygame.display.Info()
blockW = screenInfo.current_h // 40
screenH = blockW * 25
screenW = blockW * 20
screen = pygame.display.set_mode((screenW, screenH), 0, 32)
pygame.display.set_caption("GeoTheR's 2048")
clock = pygame.time.Clock()
lastGame = 0

block = (
    ("", "#FFFFFF"),
    ("2", "#B7E3E4"), ("4", "#167C80"), ("8", "#32B67A"), ("16", "#9C9CDD"),
    ("32", "#EDB5BD"), ("64", "#2C3979"), ("128", "#3C485E"), ("256", "#12162D"),
    ("512", "#EF5B09"), ("1024", "#384D9D"), ("2048", "#FF4C0E")
)
board = [[0 for _ in range(4)] for __ in range(4)]
blockW *= 5
__tmpBlockW = int(float(blockW) * 0.05)
pos = [[] for _ in range(4)]
for i in range(4):
    for j in range(4):
        pos[i].append((j * blockW + __tmpBlockW, blockW + i * blockW + __tmpBlockW,
                       blockW - (__tmpBlockW << 1), blockW - (__tmpBlockW << 1)))
myFont = pygame.font.SysFont("cambria", blockW // 5 * 2)
blockText = [myFont.render(block[_][0], True,
                           (255 - int(block[_][1][1: 3], 16),
                            255 - int(block[_][1][3: 5], 16),
                            255 - int(block[_][1][5: 7], 16)))
             for _ in range(12)]
myFont = pygame.font.SysFont("cambria", blockW // 5 * 1)
playingText = myFont.render("Use 'w, a, s, d' to move the tiles.", True, "#371722")
waitText = myFont.render("Push 'space' to start.", True, "#EF3E4A")
myFont = pygame.font.SysFont("cambria", blockW // 5 * 2)
winText = myFont.render("You win!", True, "#20AD65")
failText = myFont.render("Track lost.", True, "#EF3E4A")


def handle(_opt):
    global board
    if _opt == 1:
        for j in range(4):
            for i in range(1, 4):
                if board[i][j]:
                    ind = i
                    while ind > 0:
                        if not board[ind - 1][j]:
                            board[ind - 1][j] = board[ind][j]
                            board[ind][j] = 0
                        elif board[ind - 1][j] == board[ind][j]:
                            board[ind - 1][j] += 1
                            board[ind][j] = 0
                            break
                        else:
                            break
                        ind -= 1
    elif _opt == 2:
        for j in range(4):
            for i in range(2, -1, -1):
                if board[i][j]:
                    ind = i
                    while ind < 3:
                        if not board[ind + 1][j]:
                            board[ind + 1][j] = board[ind][j]
                            board[ind][j] = 0
                        elif board[ind + 1][j] == board[ind][j]:
                            board[ind + 1][j] += 1
                            board[ind][j] = 0
                            break
                        else:
                            break
                        ind += 1
    elif _opt == 3:
        for i in range(4):
            for j in range(1, 4):
                if board[i][j]:
                    ind = j
                    while ind > 0:
                        if not board[i][ind - 1]:
                            board[i][ind - 1] = board[i][ind]
                            board[i][ind] = 0
                        elif board[i][ind - 1] == board[i][ind]:
                            board[i][ind - 1] += 1
                            board[i][ind] = 0
                            break
                        else:
                            break
                        ind -= 1
    elif _opt == 4:
        for i in range(4):
            for j in range(2, -1, -1):
                if board[i][j]:
                    ind = j
                    while ind < 3:
                        if not board[i][ind + 1]:
                            board[i][ind + 1] = board[i][ind]
                            board[i][ind] = 0
                        elif board[i][ind + 1] == board[i][ind]:
                            board[i][ind + 1] += 1
                            board[i][ind] = 0
                            break
                        else:
                            break
                        ind += 1

    for i in range(4):
        for j in range(4):
            if board[i][j] == 11:
                return 1

    tmp = [(i, j) for i in range(4) for j in range(4) if not board[i][j]]
    cnt = len(tmp)
    if cnt:
        geneTarget = random.randint(0, cnt - 1)
        board[tmp[geneTarget][0]][tmp[geneTarget][1]] = 1 if geneTarget & 1 else 2
    if cnt <= 1:
        for i in range(1, 4):
            for j in range(1, 4):
                if board[i][j] == board[i - 1][j] or board[i][j] == board[i][j - 1]:
                    return 0
        for i in range(1, 4):
            if board[i][0] == board[i - 1][0] or board[0][i] == board[0][i - 1]:
                return 0
        return -1
    return 0


def calTextPos(txt, ps):
    W = txt.get_width()
    H = txt.get_height()
    return ps[0] + ((ps[2] - W) >> 1), ps[1] + ((ps[3] - H) >> 1)


def updateScreen():
    global screen
    screen.fill("#F9F7E8")
    for i in range(4):
        for j in range(4):
            now = board[i][j]
            pygame.draw.rect(screen, block[now][1], pos[i][j], 0, border_radius=10)
            screen.blit(blockText[now], calTextPos(blockText[now], pos[i][j]))


def mainLoop():
    opt = 1
    global board, lastGame
    board = [[0 for _ in range(4)] for __ in range(4)]
    while True:
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_w:
                    opt = 1
                if event.key == pygame.K_s:
                    opt = 2
                if event.key == pygame.K_a:
                    opt = 3
                if event.key == pygame.K_d:
                    opt = 4
        if opt != 0:
            sta = handle(opt)
            updateScreen()
            if sta == -1:
                screen.blit(failText, calTextPos(failText, (0, 0, blockW * 4, blockW)))
                lastGame = -1
                break
            elif sta == 1:
                screen.blit(winText, calTextPos(winText, (0, 0, blockW * 4, blockW)))
                lastGame = 1
                break
            else:
                screen.blit(playingText, calTextPos(playingText, (0, 0, blockW * 4, blockW)))
            pygame.display.flip()
            opt = 0
        clock.tick(100)
    pygame.display.flip()


def enter():
    while True:
        clock.tick()
        screen.fill("#F9F7E8")
        if lastGame == 1:
            screen.blit(winText, calTextPos(winText, (0, 0, blockW * 4, blockW)))
        elif lastGame == -1:
            screen.blit(failText, calTextPos(failText, (0, 0, blockW * 4, blockW)))
        for i in range(4):
            for j in range(4):
                now = board[i][j]
                pygame.draw.rect(screen, block[now][1], pos[i][j], 0, border_radius=10)
                screen.blit(blockText[now], calTextPos(blockText[now], pos[i][j]))
        tmp = pygame.Surface((blockW << 2, blockW << 2))
        tmp.set_alpha(128)
        tmp.fill("#F0CF61")
        screen.blit(tmp, (0, blockW))
        screen.blit(waitText, calTextPos(waitText, (0, blockW, blockW << 2, blockW << 2)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == KEYDOWN and event.key == pygame.K_SPACE:
                mainLoop()
                break
        clock.tick(24)


enter()
