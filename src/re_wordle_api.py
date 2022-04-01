"""
Copyright (C) 2022  Sam Wagenaar, Dakota Goldberg

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import random
from string import ascii_lowercase
import os
import sys

# Color codes
GREEN = "@"
YELLOW = "#"
WHITE = "$"
DARK = "%"
RESET = "^"


def license_notice():
    return """
Copyright (C) 2022  Sam Wagenaar, Dakota Goldberg

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


def show_license_notice():
    print(license_notice())


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    default = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    base_path = getattr(sys, '_MEIPASS', default)
    return os.path.join(base_path, relative_path)


class Wordle:

    def __init__(self):
        self.wordList = []
        self.word = None
        self.correct = False
        self.guesses = []

    # Create word list
    def gen_list(self, length):
        words = []
        lines = open(resource_path('assets/full_dictionary.txt')).read().splitlines()
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
        while len(self.word) < 2 or len(self.word) > 7:
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
