# By Sam Wagenaar
import pygame
import wordle_api
import random
import string
import time

pygame.init()

screen = pygame.display.set_mode([600, 600])
pygame.display.set_caption("Wordle")
if random.randint(0, 1000) == 0:  # Easter eggs!
    pygame.display.set_caption(
        chr(127757) + chr(127758) + chr(127759) + "Worlde" + chr(127757) + chr(127758) + chr(127759))

font = pygame.font.Font("FantasqueSansMono-Regular.ttf", 48)

GREEN_COLOR = (49, 231, 34)
YELLOW_COLOR = (255, 255, 85)
WHITE_COLOR = (175, 175, 175)
DARK_COLOR = (75, 75, 75)
RESET_COLOR = (255, 255, 255)

color_by_code = {
    "g": GREEN_COLOR,
    "y": YELLOW_COLOR,
    "w": WHITE_COLOR,
    "d": DARK_COLOR,
    "r": RESET_COLOR
}


def render_word(word, pos):
    x = pos[0]
    y = pos[1]
    max_height = 0
    max_width = 0
    color = RESET_COLOR
    word = word.upper() \
        .replace(wordle_api.GREEN, "g") \
        .replace(wordle_api.YELLOW, "y") \
        .replace(wordle_api.WHITE, "w") \
        .replace(wordle_api.DARK, "d") \
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
        max_width = max(max_width, max(letter_rect.width, underscore_rect.width))
    return max_height


def gen_keyboard_line(line):
    text = ""
    for let in line:
        num = line[let]
        if num == -1:
            text += wordle_api.RESET
        elif num == 0:
            text += wordle_api.DARK
        elif num == 1:
            text += wordle_api.YELLOW
        elif num == 2:
            text += wordle_api.GREEN
        else:
            raise IndexError("Number " + num + " is an invalid code")
        text += let
    return text


def render_keyboard(top, middle, bottom, pos):
    x = pos[0]
    y = pos[1]
    # Letter width 25
    y += render_word(gen_keyboard_line(top), (x, y)) + 15
    y += render_word(gen_keyboard_line(middle), (x + 12, y)) + 15
    y += render_word(gen_keyboard_line(bottom), (x + 37, y)) + 15


def run_game():
    play_again = False
    wordle = wordle_api.Wordle()
    # change to pick_word_reasonable_length for more random lengths while being sensible
    # wordle.pick_word_from_length(5)
    wordle.pick_word_reasonable_length()

    print(f"List length: {len(wordle.wordList)}\nWord Length: {len(wordle.word)}")

    # Setup keyboard
    l1 = "QWERTYUIOP"
    l2 = "ASDFGHJKL"
    l3 = "ZXCVBNM"
    line_1 = {x: -1 for x in l1}
    line_2 = {x: -1 for x in l2}
    line_3 = {x: -1 for x in l3}

    typed_word = ""

    kg = True
    red_flash_end = 0
    interactable = True
    while kg:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                kg = False
            elif event.type == pygame.KEYDOWN:
                if interactable:
                    if event.key == pygame.K_BACKSPACE:
                        typed_word = typed_word[:-1]
                    elif event.key == pygame.K_RETURN:
                        if wordle.is_valid_length(typed_word) and wordle.is_valid_guess(typed_word):
                            # update keyboard
                            grey, yellow, green = wordle.generate_letter_accuracies(typed_word)
                            for k in grey:
                                k = k.upper()
                                if k in line_1:
                                    line_1[k] = max(0, line_1[k])
                                if k in line_2:
                                    line_2[k] = max(0, line_2[k])
                                if k in line_3:
                                    line_3[k] = max(0, line_3[k])
                            for k in yellow:
                                k = k.upper()
                                if k in line_1:
                                    line_1[k] = max(1, line_1[k])
                                if k in line_2:
                                    line_2[k] = max(1, line_2[k])
                                if k in line_3:
                                    line_3[k] = max(1, line_3[k])
                            for k in green:
                                k = k.upper()
                                if k in line_1:
                                    line_1[k] = max(2, line_1[k])
                                if k in line_2:
                                    line_2[k] = max(2, line_2[k])
                                if k in line_3:
                                    line_3[k] = max(2, line_3[k])

                            # update guesses and reset
                            wordle.guesses.append(typed_word)
                            typed_word = ""
                        else:
                            red_flash_end = time.time() + 2
                    else:
                        letter = event.unicode.lower()
                        if letter != "" and letter in string.ascii_lowercase and len(typed_word) < len(wordle.word):
                            typed_word += letter
                else:
                    if event.key == pygame.K_RETURN:
                        play_again = True
                        kg = False
                    elif event.key == pygame.K_q:
                        play_again = False
                        kg = False

        # Render
        screen.fill((0, 0, 0))
        if time.time() < red_flash_end:
            screen.fill((100, 0, 0))

        wx = 20
        wy = 20
        for guess in wordle.guesses:
            wy += render_word(wordle.generate_response(guess), (wx, wy)) + 15
        if len(wordle.guesses) < 6 and (len(wordle.guesses) == 0 or wordle.guesses[-1] != wordle.word):
            render_word(typed_word + " " * (len(wordle.word) - len(typed_word)), (wx, wy))
            render_keyboard(line_1, line_2, line_3, (115, 410))
        else:
            if wordle.guesses[-1] == wordle.word:
                wy += render_word(f"{wordle_api.GREEN}CONGRATULATIONS!{wordle_api.RESET}", (wx, wy)) + 15
            else:
                if interactable:
                    red_flash_end = time.time() + 2
                wy += render_word(f"{wordle_api.YELLOW}INCORRECT{wordle_api.RESET}", (wx, wy)) + 15
                wy += render_word(f"{wordle_api.WHITE}THE WORD WAS{wordle_api.RESET}", (wx, wy)) + 15
                wy += render_word(wordle_api.GREEN + wordle.word + wordle_api.RESET, (wx, wy)) + 15
            interactable = False
        pygame.display.update()
    return play_again


keep_playing = run_game()
while keep_playing:
    keep_playing = run_game()
pygame.quit()
