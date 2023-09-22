"""
Stores information about the state of the game. Determines valid moves at each turn.
Keeps track of moves throughout the game.
"""

import pygame as p
import time
import random
from wordList import WordList


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
    clock = p.time.Clock()
    p.display.set_mode((0, 0), p.FULLSCREEN)
    WIDTH, HEIGHT = p.display.get_surface().get_size()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    SQ_HEIGHT = HEIGHT // 14
    SQ_WIDTH = WIDTH // 10
    MAX_FPS = 15
    p.display.set_caption("Main Menu")
    run = True
    font = p.font.SysFont("Helvitca", 60, False, False)
    play = Button(4 * SQ_WIDTH, 5 * SQ_HEIGHT,
                  SQ_WIDTH * 2, SQ_HEIGHT, "Play", True)
    quit = Button(4 * SQ_WIDTH, 7 * SQ_HEIGHT,
                  SQ_WIDTH * 2, SQ_HEIGHT, "Quit", False)
    while run:
        screen.fill((10, 10, 10))
        drawText(screen, "Welcome to Wordle!", font,
                 (255, 255, 255), SQ_WIDTH * 3.65, SQ_HEIGHT)
        drawText(screen, "Ready to Play?", font, (255, 255, 255),
                 SQ_WIDTH * 4, 2 * SQ_HEIGHT)
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
    word = WordList.wordList[random.randint(0, len(WordList.wordList) - 1)]
    wordleFont = p.font.SysFont("Helvitca", 100, False, False)
    user_text = ""
    input_rect = p.Rect(SQ_WIDTH * 3.9, SQ_HEIGHT * 8,
                        SQ_WIDTH * 2.2, SQ_HEIGHT * 1)
    quit = Button(4 * SQ_WIDTH, 11 * SQ_HEIGHT,
                  SQ_WIDTH * 2, SQ_HEIGHT, "Quit", False)
    guessed = False
    print(word)
    while run:
        for e in p.event.get():
            if e.type == p.QUIT:
                run = False
                return
            if e.type == p.KEYDOWN:
                if e.key == p.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif e.key == p.K_RETURN:
                    user_guess = user_text
                    user_text = ""
                    guessed = True
                else:
                    if len(user_text) < 5 and e.unicode.isalpha():
                        user_text += e.unicode.upper()

        if not run:
            return
        screen.fill((10, 10, 10))
        if guessed:
            wordDictArr = []
            for i in range(len(user_guess)):
                if user_guess[i] == word[i]:
                    wordDictArr.append({i: [user_guess[i], "green"]})
                elif user_guess[i] in word:
                    wordDictArr.append({i: [user_guess[i], "yellow"]})
                else:
                    wordDictArr.append({i: [user_guess[i], "gray"]})
            print(wordDictArr)
            guessed = False
        color = p.Color(50, 50, 50)
        p.draw.rect(screen, color, input_rect)
        run = quit.process(screen)
        text_surface = wordleFont.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x, input_rect.y))
        p.display.flip()
        clock.tick(60)
        p.display.update()


if __name__ == "__main__":
    main()
