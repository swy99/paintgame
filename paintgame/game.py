import pygame, random, sys

size = [1280, 720]
MAXMOVES = 40
white = (255,255,255)
red = (251,0,0)
orange = (232,135,17)
yellow = (222,236,57)
green = (49,167,42)
colors = [red, orange, yellow, green]
keys = [pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4]
screen = pygame.display.set_mode(size)

class Square:
    def __init__(self,x,y,w,h,color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
    def changecolor(self, col):
        self.color = col
    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x,self.y,self.w,self.h])
    def paint(self, col):
        initialcolor = self.color
        self.changecolor(col)
        self.draw()
        return initialcolor

class Board:
    def __init__(self):
        self.tiles = []
        for i in range(32):
            self.tiles.append([])
            for j in range(18):
                self.tiles[i].append(Square(i*40,j*40,40,40,random.choice(colors)))
                self.tiles[i][j].draw()
        screen.blit(pygame.image.load("paint.png"),(7,6))
    def paint(self,col):
        oldcol = self.tiles[0][0].color
        cand = []
        for i in range(32):
            for j in range(18):
                if self.tiles[i][j].color == oldcol:
                    cand.append((i,j))
        self.tiles[0][0].paint(col)
        self.paintadj(cand,0,0,col)
    def paintadj(self, cand, x, y, col):
        if (x-1,y) in cand:
            cand.remove((x-1,y))
            self.tiles[x-1][y].paint(col)
            self.paintadj(cand, x-1, y, col)
        if (x+1,y) in cand:
            cand.remove((x+1,y))
            self.tiles[x+1][y].paint(col)
            self.paintadj(cand, x+1, y, col)
        if (x,y-1) in cand:
            cand.remove((x,y-1))
            self.tiles[x][y-1].paint(col)
            self.paintadj(cand, x, y-1, col)
        if (x,y+1) in cand:
            cand.remove((x,y+1))
            self.tiles[x][y+1].paint(col)
            self.paintadj(cand, x, y+1, col)
    def iswin(self):
        col = self.tiles[0][0].color
        for i in range(32):
            for j in range(18):
                if self.tiles[i][j].color != col: return False
        return True

def main():
    pygame.init()
    movesleft = MAXMOVES
    pygame.display.set_caption("색채우기 (%d회 남음)" % movesleft)
    screen.fill(white)
    board = Board()

    done = False
    while not done and movesleft > 0:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in keys:
                    board.paint(colors[keys.index(event.key)])
                    screen.blit(pygame.image.load("paint.png"), (7, 6))
                    movesleft -= 1
                    pygame.display.set_caption("색채우기 (%d회 남음)" % movesleft)
                    if board.iswin():
                        print('Congratulations! You won with %d moves!' % (MAXMOVES - movesleft))
                        done = True
                        break
                    if movesleft == 0:
                        print('Game Over')
                        done = True
                        break
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()