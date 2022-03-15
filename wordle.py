# Original by Dakota Goldberg
# Modified by Sam Wagenaar
import random
from colorama import Fore, Back, Style
from string import ascii_lowercase

wordCorrect = False
guesses = []


# Create word list
def gen_list(length):
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
    return words


tmpWord = random.choice(gen_list(-1))
wordLength = len(tmpWord)

word_list = gen_list(wordLength)

print(f"List length: {len(word_list)}\nWord Length: {wordLength}")
'''for x in range(1, 25):
    tmp = gen_list(x)
    print(f"[{x}]: {len(tmp)} {tmp}")'''


def select_word():
    # lines = open('dictionary.txt').read().splitlines()
    return random.choice(word_list)  # lines)


word = select_word().lower()
print(word)


def is_valid_word(word_guess):
    return word_guess in word_list  # open('dictionary.txt').read().splitlines()


def paint_accuracy(guess_word, answer_word):
    letters_available = {}
    for letter in answer_word:
        if letter not in letters_available:
            letters_available[letter] = 0
        letters_available[letter] += 1

    for i in range(len(guess_word)):
        if guess_word[i] == answer_word[i]:
            letters_available[guess_word[i]] -= 1

    for i in range(len(guess_word)):
        if guess_word[i] == answer_word[i]:
            print(Fore.GREEN + guess_word[i], end="")
        elif guess_word[i] in answer_word and letters_available[guess_word[i]] > 0:
            print(Fore.YELLOW + guess_word[i], end="")
            letters_available[guess_word[i]] -= 1
        else:
            print(Fore.WHITE + guess_word[i], end="")
    print(Style.RESET_ALL)


while not wordCorrect:
    if len(guesses) == 6:
        print(Fore.WHITE + f"Sorry, you only have 6 chances to guess. The word was \"{word}\"." + Style.RESET_ALL)
        break
    guess = input(Fore.WHITE + f"\nGuess #{len(guesses) + 1}/6: enter a word: " + Style.RESET_ALL).lower()
    if len(guess) != wordLength:
        print(f"Your word must be {wordLength} letters!")
        continue
    elif not is_valid_word(guess):
        print("Sorry, that word is not in our dictionary!")
        continue
    guesses.append(guess)
    for g in guesses:
        paint_accuracy(g, word)
    if word == guess:
        print("Congratulations!")
        wordCorrect = True
