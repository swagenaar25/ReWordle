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
from colorama import Fore, Style
import re_wordle_api

re_wordle_api.show_license_notice()

wordle = re_wordle_api.Wordle()
wordle.pick_word_any_length()

print(f"List length: {len(wordle.wordList)}\nWord Length: {len(wordle.word)}")
'''for x in range(1, 25):
    tmp = gen_list(x)
    print(f"[{x}]: {len(tmp)} {tmp}")'''


def paint_accuracy(guess_word):
    text = wordle.generate_response(guess_word) \
        .replace(re_wordle_api.GREEN, Fore.GREEN) \
        .replace(re_wordle_api.YELLOW, Fore.YELLOW) \
        .replace(re_wordle_api.WHITE, Fore.WHITE) \
        .replace(re_wordle_api.RESET, Style.RESET_ALL)
    print(text)


paint_accuracy(wordle.word)

while not wordle.correct:
    if len(wordle.guesses) == 6:
        print(
            Fore.WHITE + f"Sorry, you only have 6 chances to guess. The word was \"{wordle.word}\"." + Style.RESET_ALL)
        break
    guess = input(Fore.WHITE + f"\nGuess #{len(wordle.guesses) + 1}/6: enter a word: " + Style.RESET_ALL).lower()
    if not wordle.is_valid_length(guess):
        print(f"Your word must be {len(wordle.word)} letters!")
        continue
    elif not wordle.is_valid_guess(guess):
        print("Sorry, that word is not in our dictionary!")
        continue
    wordle.guesses.append(guess)
    for g in wordle.guesses:
        paint_accuracy(g)
    if wordle.word == guess:
        print(Fore.YELLOW + "Congratulations!" + Style.RESET_ALL)
        wordle.correct = True
