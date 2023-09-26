words = open("words.txt", "r")
wordList = words.read().split("\n")
words.close()


class WordList:
    wordList = [word for word in wordList if len(word) == 5]
