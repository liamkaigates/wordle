"""
Stores information about the state of the game. Determines valid moves at each turn.
Keeps track of moves throughout the game.
"""

import pygame as p
import time


def drawText(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


class Button():
    def __init__(self, x, y, width, height, buttonText, isHuman, onePress=False, quitting=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onePress = onePress
        self.alreadyPressed = False
        self.isHuman = isHuman
        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        font = p.font.SysFont("Helvitca", 40, False, False)
        self.buttonSurface = p.Surface((self.width, self.height))
        self.buttonRect = p.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

    def process(self, screen):
        mousePos = p.mouse.get_pos()
        run = True
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if p.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    run = False
                elif not self.alreadyPressed:
                    run = False
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)
        return run


def main():
    p.init()
    p.display.set_mode((0, 0), p.FULLSCREEN)
    WIDTH, HEIGHT = p.display.get_surface().get_size()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    DIMENSION = 10
    SQ_SIZE = HEIGHT // DIMENSION
    MAX_FPS = 15
    p.display.set_caption("Main Menu")
    run = True
    font = p.font.SysFont("Helvitca", 60, False, False)
    play = Button(7 * SQ_SIZE, 4 * SQ_SIZE, SQ_SIZE *
                  2, SQ_SIZE, "Play", True)
    quit = Button(7 * SQ_SIZE, 6 * SQ_SIZE,
                  SQ_SIZE * 2, SQ_SIZE, "Quit", False)
    while run:
        screen.fill((10, 10, 10))
        drawText(screen, "Welcome to Wordle!", font,
                 (255, 255, 255), SQ_SIZE * 5.85, SQ_SIZE)
        drawText(screen, "Ready to Play?", font, (255, 255, 255),
                 SQ_SIZE * 6.5, 2 * SQ_SIZE)
        run = quit.process(screen)
        if run:
            run = play.process(screen)
        else:
            return
        for e in p.event.get():
            if e.type == p.QUIT:
                run = False
                return
        p.display.update()
    run = True
    time.sleep(0.25)
    p.event.clear()
    p.display.set_caption("Wordle")
    while run:
        screen.fill((10, 10, 10))
        for e in p.event.get():
            if e.type == p.QUIT:
                run = False
                return
        p.display.update()


if __name__ == "__main__":
    main()
