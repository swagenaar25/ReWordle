# Original by Dakota Goldberg
# Modified by Sam Wagenaar
import random
from colorama import Fore, Back, Style
import wordle_api

wordle = wordle_api.Wordle()
wordle.pick_word_any_length()

print(f"List length: {len(wordle.wordList)}\nWord Length: {len(wordle.word)}")
'''for x in range(1, 25):
    tmp = gen_list(x)
    print(f"[{x}]: {len(tmp)} {tmp}")'''


def paint_accuracy(guess_word):
    text = wordle.generate_response(guess_word) \
        .replace(wordle_api.GREEN, Fore.GREEN) \
        .replace(wordle_api.YELLOW, Fore.YELLOW) \
        .replace(wordle_api.WHITE, Fore.WHITE) \
        .replace(wordle_api.RESET, Style.RESET_ALL)
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
