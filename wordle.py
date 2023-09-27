"""
Stores information about the state of the game. Determines valid moves at each turn.
Keeps track of moves throughout the game.
"""

import pygame as p
import time
import sys
import random
from pygame.locals import *
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

    def process(self, screen, endQuit=False):
        mousePos = p.mouse.get_pos()
        run = True
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if p.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    run = False
                    if endQuit:
                        exit(0)
                elif not self.alreadyPressed:
                    run = False
                    self.alreadyPressed = True
                    if endQuit:
                        exit(0)
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
    word = WordList.wordList[random.randint(
        0, len(WordList.wordList) - 1)].upper()
    wordleFont = p.font.SysFont("Helvitca", 100, False, False)
    invalidFont = p.font.SysFont("Helvitca", 75, True, False)
    gray_color = p.Color(50, 50, 50)
    green_color = p.Color(0, 128, 0)
    yellow_color = p.Color(255, 196, 37)
    user_text = ""
    input_rect = p.Rect(SQ_WIDTH * 3.9, SQ_HEIGHT * 9,
                        SQ_WIDTH * 2.2, SQ_HEIGHT * 1)
    invalid_rect = p.Rect(SQ_WIDTH * 2.7, SQ_HEIGHT * 4,
                          SQ_WIDTH * 4.4, SQ_HEIGHT * 2)
    invalid_guess = [False, False]
    invalid_count = 60
    word_output_rect = [[[p.Rect(SQ_WIDTH * (3.75 + i * 0.5), SQ_HEIGHT * (1 + j * 1.25),
                        SQ_WIDTH * 0.5, SQ_HEIGHT * 1.25), gray_color, ""] for i in range(5)] for j in range(6)]
    quit = Button(4 * SQ_WIDTH, 11 * SQ_HEIGHT,
                  SQ_WIDTH * 2, SQ_HEIGHT, "Quit", False)
    guessed = False
    endGame = False
    guessedWords = []
    playAgain = Button(4 * SQ_WIDTH, 7 * SQ_HEIGHT,
                       SQ_WIDTH * 2, SQ_HEIGHT, "Play Again", False)
    playAgainRect = p.Rect(SQ_WIDTH * 3.9, SQ_HEIGHT * 4,
                           SQ_WIDTH * 2.2, SQ_HEIGHT * 1.5)
    lost_word_rect = p.Rect(SQ_WIDTH * 2.2, SQ_HEIGHT * 2,
                            SQ_WIDTH * 5.4, SQ_HEIGHT * 1.5)
    user_guess = ""
    numGuess = 0
    text = ""
    playAgainBool = True
    lost = False
    while run:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            if e.type == p.KEYDOWN:
                if e.key == p.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif e.key == p.K_RETURN:
                    if len(user_text) == 5:
                        user_guess = user_text
                        if user_guess in guessedWords or user_guess.lower() not in WordList.wordList:
                            invalid_guess = [
                                user_guess in guessedWords, user_guess.lower() not in WordList.wordList]
                        else:
                            guessed = True
                            user_text = ""
                            guessedWords.append(user_guess)
                else:
                    if len(user_text) < 5 and e.unicode.isalpha():
                        user_text += e.unicode.upper()
        screen.fill((10, 10, 10))
        quitBool = quit.process(screen)
        if not quitBool:
            run = False
        p.draw.rect(screen, gray_color, input_rect)
        for i in range(6):
            for j in range(5):
                p.draw.rect(
                    screen, word_output_rect[i][j][1], word_output_rect[i][j][0])
                guess_surface = wordleFont.render(
                    word_output_rect[i][j][2], True, (255, 255, 255))
                screen.blit(
                    guess_surface, (word_output_rect[i][j][0].x + 7.5, word_output_rect[i][j][0].y))
        text_surface = wordleFont.render(user_text, True, (255, 255, 255))
        if guessed:
            wordDictArr = [[], [], [], [], []]
            letterCountDict = {word[i]: word.count(
                word[i]) for i in range(len(word))}
            letterGuessDict = {i: [0, user_guess[i]]
                               for i in range(len(user_guess))}
            for i in range(len(user_guess)):
                if user_guess[i] == word[i]:
                    wordDictArr[i] = [user_guess[i], green_color]
                    letterCountDict[user_guess[i]] -= 1
                    letterGuessDict[i][0] += 1
            for i in range(len(user_guess)):
                if user_guess[i] in word and user_guess[i] != word[i] and letterCountDict[user_guess[i]] > 0:
                    wordDictArr[i] = [user_guess[i], yellow_color]
                    letterCountDict[user_guess[i]] -= 1
                    letterGuessDict[i][0] += 1
            for i in range(len(user_guess)):
                if user_guess[i] not in word:
                    wordDictArr[i] = [user_guess[i], gray_color]
                    letterGuessDict[i][0] += 1
                elif user_guess[i] in word and 0 == letterGuessDict[i][0]:
                    wordDictArr[i] = [user_guess[i], gray_color]
                    letterGuessDict[i][0] += 1
            guess_surface = wordleFont.render(
                user_guess, True, (255, 255, 255))
            for i in range(len(wordDictArr)):
                word_output_rect[numGuess][i][1] = wordDictArr[i][1]
                word_output_rect[numGuess][i][2] = wordDictArr[i][0]
            guessed = False
            numGuess += 1
        screen.blit(text_surface, (input_rect.x, input_rect.y))
        clock.tick(60)
        if invalid_guess[0] or invalid_guess[1]:
            p.draw.rect(screen, gray_color, invalid_rect)
            if invalid_guess[0]:
                invalid_surface = invalidFont.render(
                    "ALREADY GUESSED", True, (255, 255, 255))
                screen.blit(
                    invalid_surface, (invalid_rect.x + SQ_WIDTH * 0.15, invalid_rect.y + SQ_HEIGHT * 0.5))
            elif invalid_guess[1]:
                invalid_surface = invalidFont.render(
                    "NOT IN WORD LIST", True, (255, 255, 255))
                screen.blit(
                    invalid_surface, (invalid_rect.x + SQ_WIDTH * 0.15, invalid_rect.y + SQ_HEIGHT * 0.5))
            if invalid_count == 0:
                invalid_count = 60
                invalid_guess = [False, False]
            else:
                invalid_count -= 1
        if numGuess == 6 or word == user_guess or endGame:
            if word == user_guess:
                text = "You Win"
            elif numGuess == 6:
                text = "You Lose"
                lost = True
            p.draw.rect(screen, p.Color(0, 0, 0), playAgainRect)
            play_again_surface = invalidFont.render(
                text, True, (255, 255, 255))
            screen.blit(
                play_again_surface, (playAgainRect.x + SQ_WIDTH * 0.25, playAgainRect.y + SQ_HEIGHT * 0.4))
            if lost:
                p.draw.rect(screen, p.Color(0, 0, 0), lost_word_rect)
                lost_surface = invalidFont.render(
                    "The word was " + word, True, (255, 255, 255))
                screen.blit(
                    lost_surface, (lost_word_rect.x + SQ_WIDTH * 0.3, lost_word_rect.y + SQ_HEIGHT * 0.4))
            endGame = True
            numGuess = 0
            user_guess = ""
            playAgainBool = playAgain.process(screen)
            if not playAgainBool:
                endGame = False
                run = True
                word = WordList.wordList[random.randint(
                    0, len(WordList.wordList) - 1)].upper()
                word_output_rect = [[[p.Rect(SQ_WIDTH * (3.75 + i * 0.5), SQ_HEIGHT * (1 + j * 1.25),
                                             SQ_WIDTH * 0.5, SQ_HEIGHT * 1.25), gray_color, ""] for i in range(5)] for j in range(6)]
                guessedWords = []
                invalid_guess = [False, False]
                lost = False
        p.display.flip()
        quitBool = quit.process(screen, endQuit=True)
        if not quitBool:
            run = False


if __name__ == "__main__":
    main()
