import random
from colorama import Fore, Back, Style
wordCorrect = False
guesses = []
numGuess = 1

def selectWord():
    lines = open('dictionary.txt').read().splitlines()
    chosenWord = random.choice(lines)
    return chosenWord

word = selectWord().lower()

def isWord(wordGuess):
    return wordGuess in open('dictionary.txt').read().splitlines()

def paintAccuracy(guess, word):
    for i in range(len(guess)):
        if guess[i] == word[i]:
            print(Fore.GREEN + guess[i], end="")
        elif guess[i] in word:
            print(Fore.YELLOW + guess[i], end="")
        else:
            print(Fore.WHITE + guess[i], end="")
    print("")


while (not wordCorrect):
    if (numGuess == 7):
        print(Fore.WHITE + f"Sorry, you only have 6 chances to guess. The word was \"{word}\".")
        break
    guess = input(Fore.WHITE + f"\nGuess #{numGuess}/6: enter a word: ").lower()
    if (len(guess) != 5):
        print("Your word must be 5 letters!")
        continue
    elif (not isWord(guess)):
        print("Sorry, that word is not in our dictionary!")
        continue
    numGuess+=1
    guesses.append(guess);
    for g in guesses:
        paintAccuracy(g, word)
    if word == guess:
        print("Congratulations!")
        wordCorrect = True

