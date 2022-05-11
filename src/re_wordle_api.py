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
import urllib.request
import os

# Color codes
GREEN = "@"
YELLOW = "#"
WHITE = "$"
DARK = "%"
RESET = "^"


def clear_color_codes(text: str) -> str:
    return text.replace(GREEN, "").replace(YELLOW, "").replace(WHITE, "").replace(DARK, "").replace(RESET, "")


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


def external_path(relative_path: str) -> str:
    is_frozen = getattr(sys, 'frozen', False)
    if is_frozen:
        return os.path.join(os.path.dirname(os.path.abspath(sys.executable)), relative_path)
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", relative_path)


class Wordle:

    def __init__(self):
        self.wordList = []
        self.word = None
        self.correct = False
        self.guesses = []
        self.language = ""
        self.languages = {}
        self._external_language_file_location = os.path.abspath(external_path(".rewordle_lang/languages.txt"))
        self.load_language_options()

    def get_language_name(self):
        try:
            return self.languages[self.language]
        except KeyError:
            return "UNKNOWN"

    def external_language_location(self, language):  # noqa
        return os.path.abspath(external_path(f".rewordle_lang/{language}"))

    def load_language_options(self) -> bool:
        """Load language options from disk

        :return: Language changed
        """
        f = open(self.language_list_location())
        languages = f.read().split("\n")
        f.close()
        self.languages.clear()
        for line in languages:
            try:
                k, v = line.split(":")
                self.languages[k] = v
            except ValueError:
                print(f"Invalid language data with line {line}")
        if self.language not in self.languages:
            self.language = list(self.languages.keys())[0]
            return True
        else:
            return False

    def download_language_data(self):
        list_url = f"https://raw.githubusercontent.com/swagenaar25/ReWordle/master/assets/languages.txt"
        urllib.request.urlretrieve(list_url, self._external_language_file_location)
        ret = self.load_language_options()
        for language in self.languages:
            urllib.request.urlretrieve(
                f"https://raw.githubusercontent.com/swagenaar25/ReWordle/master/assets/lang/{language}.txt",
                self.external_language_location(language))
        return ret

    def language_list_location(self):
        if os.path.exists(self._external_language_file_location):
            return self._external_language_file_location
        else:
            return os.path.abspath(resource_path("assets/languages.txt"))

    def word_list_location(self):
        if os.path.exists(self.external_language_location(self.language)):
            return self.external_language_location(self.language)
        else:
            return os.path.abspath(resource_path(f"assets/lang/{self.language}.txt"))

    # Create word list
    def gen_list(self, length):
        words = []
        lines = open(resource_path(self.word_list_location())).read().splitlines()
        for line in lines:
            if length == -1 or len(line) == length:
                ok = True
                for letter in line:
                    if letter not in ascii_lowercase:
                        ok = False
                if ok:
                    words.append(line)
        self.wordList = words.copy()
        return words

    def pick_word_from_length(self, length):
        self.gen_list(length)
        if len(self.wordList) == 0:
            print(f"No words found for length {length}")
            self.gen_list(-1)
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
        self.gen_list(len(self.word))

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


if __name__ == "__main__":  # If we get run, count all words
    for i in range(20):
        tmp = Wordle()
        tmp.gen_list(i)
        print(f"{len(tmp.wordList)} words of length [{i}]: {tmp.wordList}")
