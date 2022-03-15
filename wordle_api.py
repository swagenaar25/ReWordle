import random
from string import ascii_lowercase


class Wordle:

    GREEN = "$G$"
    YELLOW = "$Y$"
    WHITE = "$W$"
    RESET = "$R$"

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
                out += self.GREEN + guess_word[i]
            elif guess_word[i] in self.word and letters_available[guess_word[i]] > 0:
                out += self.YELLOW + guess_word[i]
                letters_available[guess_word[i]] -= 1
            else:
                out += self.WHITE + guess_word[i]
        out += self.RESET
        return out
