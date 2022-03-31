# Original by Dakota Goldberg
# Modified by Sam Wagenaar
import pygame
import wordle_api
import random
import string
import time

pygame.init()

screen = pygame.display.set_mode([600, 600])
pygame.display.set_caption("Wordle")
if random.randint(0, 1000) == 0:  # Easter eggs!
    pygame.display.set_caption(chr(127757)+chr(127758)+chr(127759)+"Worlde"+chr(127757)+chr(127758)+chr(127759))

wordle = wordle_api.Wordle()
wordle.pick_word_from_length(5)

print(f"List length: {len(wordle.wordList)}\nWord Length: {len(wordle.word)}")

typed_word = ""

font = pygame.font.Font("FantasqueSansMono-Regular.ttf", 48)
test_letter = font.render("HELLO", True, (0, 255, 0))
test_letter_rect = test_letter.get_rect()
test_letter_rect.centerx = 300
test_letter_rect.y = 300

GREEN_COLOR = (49, 231, 34)
YELLOW_COLOR = (255, 255, 85)
WHITE_COLOR = (175, 175, 175)
RESET_COLOR = (255, 255, 255)

color_by_code = {
    "g": GREEN_COLOR,
    "y": YELLOW_COLOR,
    "w": WHITE_COLOR,
    "r": RESET_COLOR
}


def render_word(word, pos):
    x = pos[0]
    y = pos[1]
    max_height = 0
    color = RESET_COLOR
    word = word.upper()\
        .replace(wordle_api.GREEN, "g")\
        .replace(wordle_api.YELLOW, "y")\
        .replace(wordle_api.WHITE, "w")\
        .replace(wordle_api.RESET, "r")
    for w in word:
        if w.islower():
            color = color_by_code[w]
            continue  # Don't render color code characters!
        letter_surf = font.render(w, True, color)
        letter_rect = letter_surf.get_rect()
        letter_rect.x = x
        letter_rect.y = y

        underscore_surf = font.render("_", True, (255, 255, 255))
        underscore_rect = underscore_surf.get_rect()
        underscore_rect.centerx = letter_rect.centerx
        underscore_rect.bottom = letter_rect.bottom

        screen.blit(letter_surf, letter_rect)
        screen.blit(underscore_surf, underscore_rect)

        x += underscore_rect.width + 12
        max_height = max(max_height, max(letter_rect.height, underscore_rect.height))
    return max_height


kg = True
red_flash_end = 0
interactable = True
while kg:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            kg = False
        elif event.type == pygame.KEYDOWN and interactable:
            if event.key == pygame.K_BACKSPACE:
                typed_word = typed_word[:-1]
            elif event.key == pygame.K_RETURN:
                if wordle.is_valid_length(typed_word) and wordle.is_valid_guess(typed_word):
                    wordle.guesses.append(typed_word)
                    typed_word = ""
                else:
                    red_flash_end = time.time()+2
            else:
                letter = event.unicode.lower()
                if letter != "" and letter in string.ascii_lowercase and len(typed_word) < len(wordle.word):
                    typed_word += letter
                    print(typed_word)

    # Render
    screen.fill((0, 0, 0))
    if time.time() < red_flash_end:
        screen.fill((100, 0, 0))

    wx = 20
    wy = 20
    for guess in wordle.guesses:
        wy += render_word(wordle.generate_response(guess), (wx, wy))+15
    if len(wordle.guesses) < 6:
        render_word(typed_word + " "*(len(wordle.word)-len(typed_word)), (wx, wy))
    else:
        if wordle.guesses[5] == wordle.word:
            wy += render_word(f"{wordle_api.GREEN}CORRECT!{wordle_api.RESET}", (wx, wy))+15
        else:
            wy += render_word(f"{wordle_api.YELLOW}INCORRECT{wordle_api.RESET}", (wx, wy))+15
            wy += render_word(f"{wordle_api.WHITE}THE WORD WAS{wordle_api.RESET}", (wx, wy))+15
            wy += render_word(wordle_api.GREEN+wordle.word+wordle_api.RESET, (wx, wy))+15
    pygame.display.update()


'''for x in range(1, 25):
    tmp = gen_list(x)
    print(f"[{x}]: {len(tmp)} {tmp}")'''


"""def paint_accuracy(guess_word):
    text = wordle.generate_response(guess_word) \
        .replace("$G$", Fore.GREEN) \
        .replace("$Y$", Fore.YELLOW) \
        .replace("$W$", Fore.WHITE) \
        .replace("$R$", Style.RESET_ALL)
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
"""