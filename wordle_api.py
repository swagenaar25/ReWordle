import random
from string import ascii_lowercase

GREEN = "@"
YELLOW = "#"
WHITE = "$"
DARK = "%"
RESET = "^"


class Wordle:

    def __init__(self):
        self.wordList = []
        self.word = None
        self.correct = False
        self.guesses = []

    # Create word list
    def gen_list(self, length):
        words = []
        lines = open('full_dictionary.txt').read().splitlines()
        for line in lines:
            if length == -1 or len(line) == length:
                ok = True
                for letter in line:
                    if letter not in ascii_lowercase:
                        ok = False
                if ok:
                    words.append(line)
        self.wordList = words.copy()

    def pick_word_from_length(self, length):
        self.gen_list(length)
        self.word = random.choice(self.wordList)
        self.guesses = []

    def pick_word_any_length(self):
        self.gen_list(-1)
        self.word = random.choice(self.wordList)
        self.guesses = []

    def pick_word_reasonable_length(self):
        self.pick_word_any_length()
        while 2 > len(self.word) > 9:
            self.pick_word_any_length()

    def is_valid_guess(self, guess):
        return guess in self.wordList

    def is_valid_length(self, guess):
        return len(guess) == len(self.word)

    def generate_response(self, guess_word):
        letters_available = {}
        for letter in self.word:
            if letter not in letters_available:
                letters_available[letter] = 0
            letters_available[letter] += 1

        for i in range(len(guess_word)):
            if guess_word[i] == self.word[i]:
                letters_available[guess_word[i]] -= 1

        out = ""
        for i in range(len(guess_word)):
            if guess_word[i] == self.word[i]:
                out += GREEN + guess_word[i]
            elif guess_word[i] in self.word and letters_available[guess_word[i]] > 0:
                out += YELLOW + guess_word[i]
                letters_available[guess_word[i]] -= 1
            else:
                out += WHITE + guess_word[i]
        out += RESET
        return out

    def generate_letter_accuracies(self, guess_word):
        letters_available = {}
        for letter in self.word:
            if letter not in letters_available:
                letters_available[letter] = 0
            letters_available[letter] += 1

        for i in range(len(guess_word)):
            if guess_word[i] == self.word[i]:
                letters_available[guess_word[i]] -= 1

        grey = []
        yellow = []
        green = []
        for i in range(len(guess_word)):
            if guess_word[i] == self.word[i]:
                green.append(guess_word[i])
            elif guess_word[i] in self.word and letters_available[guess_word[i]] > 0:
                yellow.append(guess_word[i])
                letters_available[guess_word[i]] -= 1
            else:
                grey.append(guess_word[i])
        return grey, yellow, green
