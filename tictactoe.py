import random
import pygame
from pygame.locals import *

#board
board=['-','-','-',
        '-','-','-',
        '-','-','-']
currPlayer='X'
winner=None
gameRunning=True

def currPlayerPlay(board,pos):
    if pos<1 or pos>9 or board[pos-1]!='-':
        return False
    else:
        board[pos-1]=currPlayer
        return True

def swapPlayer():
    global currPlayer
    if currPlayer=='O':
        currPlayer='X'
    else:
        currPlayer='O'

def computer():
    global currPlayer
    if not gameRunning:
        return
    while True:
        pos = random.randint(0, 8)
        if currPlayerPlay(board, pos):
            break  # валиден ход → излизаме от цикъла

def show_winner(text):
    winner_font = pygame.font.SysFont(None, 60)
    winner_surface = winner_font.render(text, True, (200, 0, 0))  # червен текст
    rect = winner_surface.get_rect(center=(screen_width // 2, 500))  # позиция по-долу
    displaysurf.blit(winner_surface, rect)

def checkWinner():
    global winner, gameRunning
    wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != '-':
            winner = board[a]
            #show_winner(f'Winner is {board[a]}')
            gameRunning = False
            return
    if '-' not in board:
        gameRunning = False

pygame.init()
FPS = 20
FramePerSec = pygame.time.Clock()
font=pygame.font.SysFont(None,80)

# some colors
f = (238, 224, 197)
l = (125, 64, 10)

# screen info
screen_width = 400
screen_height = 600

displaysurf = pygame.display.set_mode((screen_width, screen_height)) #размерите на полето
pygame.display.set_caption("Tic-Tac-Toe")#заглавие на играта

key_to_pos = {                  #речник кой бутон на коя позиция отговаря
    K_1: 1, K_2: 2, K_3: 3,
    K_4: 4, K_5: 5, K_6: 6,
    K_7: 7, K_8: 8, K_9: 9}

def draw_grid():
    pygame.draw.line(displaysurf, l, (50, 200), (350, 200), width=5)
    pygame.draw.line(displaysurf, l, (50, 300), (350, 300), width=5)
    pygame.draw.line(displaysurf, l, (150, 100), (150, 400), width=5)
    pygame.draw.line(displaysurf, l, (250, 100), (250, 400), width=5)

def draw_board():
    for i in range(9):
        row = i // 3
        col = i % 3
        x = 50 + col * 100
        y = 100 + row * 100
        if board[i] != '-':#ако клетката е запълнена, а показва на екрана в определеното поле
            text = font.render(board[i], True, (0, 0, 0))
            displaysurf.blit(text, (x + 30, y + 20))

error_message=""
running = True

while running:
    displaysurf.fill(f)#фона отзад
    draw_grid()#линиите на полето за игра
    draw_board()
    if error_message:
        error_font = pygame.font.SysFont(None, 32)
        lines = error_message.split('\n') #blit не поддържа автоматично \n
        y = 450
        for line in lines:
            text_surface = error_font.render(line, True, (200, 0, 0))
            displaysurf.blit(text_surface, (25, y))
            y += 30  # разстояние между редовете

    for event in pygame.event.get():
        if event.type == QUIT: #ако натисне Х
            running = False
        if gameRunning and event.type == KEYDOWN: #ако играта продължава и има натиснат клафиш
            if event.key in key_to_pos: #ако този клавиш е в речника
                pos = key_to_pos[event.key] #взимаме позицията от речника
                if currPlayerPlay(board, pos): #играем хода
                    error_message="" #няма съобщение за показване
                    checkWinner()#проверяваме дали има победител
                    if gameRunning:
                        swapPlayer() #ако играта продължава, сменяме играча
                        if currPlayer=='O':
                            computer()
                            checkWinner()
                            if gameRunning:
                                swapPlayer()
                else:
                    error_message="Избра си неправилна позиция!\n Опитай отново!" #ако играчът е избрал невалидна позиция, показваме съобщение за грешка и не сменяме играчите

    pygame.display.update() #опресняваме екрана
    FramePerSec.tick(FPS) #ограничаваме скоростта до 20 кадъра в секунда
    if not gameRunning:
        draw_board()#ако играта е приключила, проверяваме защо
        if winner:
            show_winner(f"Победител: {winner}")
        else:
            show_winner("Равенство!")
        pygame.display.update()
        pygame.time.delay(3000)  # показва резултата за 3 секунди
        running = False
pygame.quit()
