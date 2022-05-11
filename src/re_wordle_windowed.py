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
import typing
import urllib.error

import pygame
import re_wordle_api
import random
import string
import time
import colorsys

# parser = argparse.ArgumentParser()
# parser.add_argument("--letters", type=int, help="Set number of letters", default=-1)

# args = parser.parse_args()

re_wordle_api.show_license_notice()

pygame.init()

maximum_height = 0
for _, height in pygame.display.list_modes():
    maximum_height = max(maximum_height, height)


class Config:

    def __init__(self):
        self.num_letters = 0
        self.window_size = 600
        self.language = "en"
        self._testing_wordle = re_wordle_api.Wordle()

    def validate(self):
        self.num_letters = max(0, self.num_letters)
        self.window_size = max(100, min(self.window_size, maximum_height))

        self._testing_wordle.language = self.language
        self._testing_wordle.load_language_options()
        self.language = self._testing_wordle.language

    def valid_number_letters(self):
        return self.num_letters == 0 or len(self._testing_wordle.gen_list(self.num_letters)) != 0

    def update_window(self):
        global screen
        screen = pygame.display.set_mode((self.window_size, self.window_size))
        fit_font()

    def load(self):
        try:
            f = open(re_wordle_api.external_path("rewordle.conf"))
            contents = f.read()
            f.close()
            lines = contents.split("\n")
            for line in lines:
                try:
                    k, v = line.split("=")
                    if k == "num_letters":
                        self.num_letters = int(v)
                    elif k == "window_size":
                        self.window_size = int(v)
                    elif k == "language":
                        self.language = v
                except ValueError:
                    pass
        except FileNotFoundError:
            pass

    def save(self):
        f = open(re_wordle_api.external_path("rewordle.conf"), "w")
        f.write(f"num_letters={self.num_letters}\nwindow_size={self.window_size}\nlanguage={self.language}\n")
        f.close()

    def reset(self):
        default = self.__class__()
        self.window_size = default.window_size
        self.num_letters = default.num_letters
        self.language = default.language
        del default


screen = pygame.display.set_mode([600, 600])
pygame.display.set_caption("Wordle")
if random.randint(0, 200) == 0:  # Easter eggs!
    pygame.display.set_caption(
        chr(127757) + chr(127758) + chr(127759) + "Worlde" + chr(127757) + chr(127758) + chr(127759))

font_size = 48  # Fits default window, but will auto-adjust
font = pygame.font.Font(re_wordle_api.resource_path("assets/fonts/FantasqueSansMono-Regular.ttf"), font_size)
options_font = pygame.font.Font(re_wordle_api.resource_path("assets/fonts/FantasqueSansMono-Regular.ttf"),
                                int(font_size / 2))


def letter_stats(myfont):
    x = 0
    y = 0
    max_height = 0
    max_width = 0
    word = "QWERTYUIOPASDFGHJKLZXCVBNM"
    for w in word:
        letter_surf = myfont.render(w, True, (255, 255, 255))
        letter_rect = letter_surf.get_rect()
        letter_rect.x = x
        letter_rect.y = y

        underscore_surf = myfont.render("_", True, (255, 255, 255))
        underscore_rect = underscore_surf.get_rect()
        underscore_rect.centerx = letter_rect.centerx
        underscore_rect.bottom = letter_rect.bottom

        x += underscore_rect.width * 1.5
        max_height = max(max_height, max(letter_rect.height, underscore_rect.height))
        max_width = max(max_width, max(letter_rect.width, underscore_rect.width))
    return max_width, max_height


letter_width, letter_height = letter_stats(font)
vertical_spacing = letter_height / (10 / 3)
horizontal_spacing = letter_width / 2


def width(word):
    word = re_wordle_api.clear_color_codes(word)
    return (len(word) * letter_width) + ((len(word) - 1) * horizontal_spacing)


def x_for_centering(word):
    return int((screen.get_width() - width(word)) / 2)


def required_vertical_space():
    # 20 padding at top, 10 at bottom
    return ((letter_height / 5) * 3) + (
            (letter_height + vertical_spacing) * 9) - vertical_spacing  # we don't need extra spacing at the end


def required_horizontal_space():
    return width("A" * 18)


config = Config()
config.load()

def fit_font():
    global font_size, letter_width, letter_height, horizontal_spacing, vertical_spacing, font, options_font
    # Calculate required font size for window size
    # Shrink first
    while required_vertical_space() > config.window_size or required_horizontal_space() > config.window_size:
        # global font_size, font, letter_height, letter_width, horizontal_spacing, vertical_spacing
        font_size -= 1
        test_font = pygame.font.Font(re_wordle_api.resource_path("assets/fonts/FantasqueSansMono-Regular.ttf"),
                                     font_size)
        letter_width, letter_height = letter_stats(test_font)
        vertical_spacing = letter_height / (10 / 3)
        horizontal_spacing = letter_width / 2

    # Expand
    while required_vertical_space() < config.window_size and required_horizontal_space() < config.window_size:
        # global font_size, font, letter_height, letter_width, horizontal_spacing, vertical_spacing
        font_size += 1
        test_font = pygame.font.Font(re_wordle_api.resource_path("assets/fonts/FantasqueSansMono-Regular.ttf"),
                                     font_size)
        letter_width, letter_height = letter_stats(test_font)
        vertical_spacing = letter_height / (10 / 3)
        horizontal_spacing = letter_width / 2

    font = pygame.font.Font(re_wordle_api.resource_path("assets/fonts/FantasqueSansMono-Regular.ttf"), font_size)
    options_font = pygame.font.Font(re_wordle_api.resource_path("assets/fonts/FantasqueSansMono-Regular.ttf"),
                                    int(font_size / 2))
    letter_width, letter_height = letter_stats(font)
    vertical_spacing = letter_height / (10 / 3)  # noqa
    horizontal_spacing = letter_width / 2  # noqa


fit_font()
config.validate()

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
        .replace(re_wordle_api.GREEN, "g") \
        .replace(re_wordle_api.YELLOW, "y") \
        .replace(re_wordle_api.WHITE, "w") \
        .replace(re_wordle_api.DARK, "d") \
        .replace(re_wordle_api.RESET, "r")
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

        x += underscore_rect.width * 1.5
        max_height = max(max_height, max(letter_rect.height, underscore_rect.height))
        max_width = max(max_width, max(letter_rect.width, underscore_rect.width))
    # print(f"max_height:{max_height}, max_width:{max_width}")
    return max_height


def plain_text(x: int | float, y: int | float, text: str, color: typing.Tuple[int, int, int], myfont: pygame.font.Font,
               centered: bool = False, outline: bool = False):
    text_surf = myfont.render(text, True, color)
    text_rect = text_surf.get_rect()
    if centered:
        text_rect.centerx = x
        text_rect.centery = y
    else:
        text_rect.x = x
        text_rect.y = y
    screen.blit(text_surf, text_rect)
    if outline:
        box_rect = pygame.rect.Rect(text_rect.x - 2, text_rect.y - 2,
                                    text_rect.width + 4, text_rect.height + 4)
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         box_rect,
                         width=1)
        return box_rect
    return text_rect


def gen_keyboard_line(line):
    text = ""
    for let in line:
        num = line[let]
        if num == -1:
            text += re_wordle_api.RESET
        elif num == 0:
            text += re_wordle_api.DARK
        elif num == 1:
            text += re_wordle_api.YELLOW
        elif num == 2:
            text += re_wordle_api.GREEN
        else:
            raise IndexError("Number " + num + " is an invalid code")
        text += let
    return text


def render_keyboard(top, middle, bottom, pos):
    x = pos[0]
    y = pos[1]
    # Letter width 25
    top_line = gen_keyboard_line(top)
    y += render_word(top_line, (x_for_centering(top_line), y)) + vertical_spacing

    middle_line = gen_keyboard_line(middle)
    y += render_word(middle_line, (x_for_centering(middle_line), y)) + vertical_spacing

    bottom_line = gen_keyboard_line(bottom)
    y += render_word(bottom_line, (x_for_centering(bottom_line), y)) + vertical_spacing


def get_amongus(offset) -> pygame.Surface:
    """ Create amongus

    :return: Amongus surface
    """
    pattern = \
        """##..
           %##..
           ###..
           ##..""".replace("\t", "").replace(" ", "")
    surf = pygame.Surface((4, 4))
    lines = pattern.split("\n")
    body_color = colorsys.hsv_to_rgb((time.time() / 15) + offset, 1, 255)
    for x in range(4):
        for y in range(4):
            c = lines[y][x]
            color = (0, 0, 0)
            if c == "#":
                color = (int(body_color[0]), int(body_color[1]), int(body_color[2]))
            elif c == "%":
                color = (0, 255, 255)
            surf.set_at((x, y), color)
    surf.set_colorkey((0, 0, 0))
    return surf


options_text = "OPTIONS"
options_bounds = None


def run_options(wordle: re_wordle_api.Wordle) -> bool:
    """ Display options window

    :param wordle: Wordle instance to operate on
    :return: Language change
    """
    kg = True
    exit_bounds = None
    reset_bounds = None
    window_minus_bounds = None
    window_plus_bounds = None

    letter_minus_bounds = None
    letter_plus_bounds = None

    language_bounds = None

    download_list_bounds = None
    download_green_until = 0
    download_red_until = 0

    original_language = wordle.language
    while kg:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                kg = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    kg = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                size_change = 10
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    size_change = 50
                if exit_bounds is not None and exit_bounds.collidepoint(mx, my):
                    kg = False
                elif reset_bounds is not None and reset_bounds.collidepoint(mx, my):
                    config.reset()
                    config.validate()
                    wordle.language = config.language
                elif window_minus_bounds is not None and window_minus_bounds.collidepoint(mx, my):
                    config.window_size -= size_change
                    config.validate()
                    config.update_window()
                elif window_plus_bounds is not None and window_plus_bounds.collidepoint(mx, my):
                    config.window_size += size_change
                    config.validate()
                    config.update_window()
                elif letter_minus_bounds is not None and letter_minus_bounds.collidepoint(mx, my):
                    config.num_letters -= 1
                    config.validate()
                elif letter_plus_bounds is not None and letter_plus_bounds.collidepoint(mx, my):
                    config.num_letters += 1
                    config.validate()
                elif language_bounds is not None and language_bounds.collidepoint(mx, my):
                    wordle.load_language_options()
                    languages = list(wordle.languages.keys())
                    wordle.language = languages[(languages.index(wordle.language)+1) % len(languages)]
                elif download_list_bounds is not None and download_list_bounds.collidepoint(mx, my):
                    try:
                        wordle.download_language_data()
                        config.validate()
                    except urllib.error.URLError:
                        download_red_until = time.time() + 1
                    download_green_until = time.time() + 1
        screen.fill((0, 0, 0))
        exit_bounds = plain_text(5, letter_height * 0.25, "X", (255, 255, 255), options_font, outline=True)

        reset_bounds = plain_text(5, letter_height * 1.0, "RESET", (255, 255, 255), options_font, outline=True)

        # Window size
        _, _, start_offset, _ = plain_text(5, letter_height * 2.5, "Window size: ", (255, 255, 255), options_font)
        window_minus_bounds = plain_text(5 + start_offset, letter_height * 2.5, "-", (255, 255, 255), options_font,
                                         outline=True)
        gap = width(" " * 6) / 2
        plain_text(10 + (gap / 2) + start_offset, letter_height * 2.75, str(config.window_size), (255, 255, 255),
                   options_font, centered=True)
        window_plus_bounds = plain_text(5 + gap + start_offset, letter_height * 2.5, "+", (255, 255, 255), options_font,
                                        outline=True)

        # Word length
        _, _, start_offset, _ = plain_text(5, letter_height * 3.5, "Word length: ", (255, 255, 255), options_font)
        letter_minus_bounds = plain_text(5 + start_offset, letter_height * 3.5, "-", (255, 255, 255), options_font,
                                         outline=True)
        gap = width(" RANDOM ") / 2
        length_str = str(config.num_letters)
        if config.num_letters == 0:
            length_str = "RANDOM"
        plain_text(10 + (gap / 2) + start_offset, letter_height * 3.75, length_str,
                   (255, 255, 255) if config.valid_number_letters() else (255, 0, 0),
                   options_font, centered=True)
        letter_plus_bounds = plain_text(5 + gap + start_offset, letter_height * 3.5, "+", (255, 255, 255), options_font,
                                        outline=True)

        # Language selection
        _, _, start_offset, _ = plain_text(5, letter_height * 4.5, "Language: ", (255, 255, 255), options_font)
        language_bounds = plain_text(5 + start_offset, letter_height * 4.5,
                                     wordle.get_language_name(),
                                     (255, 255, 255),
                                     options_font,
                                     outline=True)

        # Word list download
        download_list_bounds = plain_text(5, letter_height * 5.5,
                                          "DOWNLOAD LANGUAGE DATA",
                                          (255, 0, 0) if time.time() < download_red_until else (
                                              GREEN_COLOR if time.time() < download_green_until else (255, 255, 255)),
                                          options_font,
                                          outline=True)
        pygame.display.update()
    config.language = wordle.language
    config.save()
    return wordle.language != original_language


def run_game():
    global options_bounds
    play_again = False
    wordle = re_wordle_api.Wordle()
    wordle.language = config.language
    wordle.load_language_options()
    config.language = wordle.language
    # change to pick_word_reasonable_length for more random lengths while being sensible
    # wordle.pick_word_from_length(5)
    if config.num_letters == 0:
        wordle.pick_word_reasonable_length()
    else:
        wordle.pick_word_from_length(config.num_letters)
    # print(wordle.word)

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
                play_again = False
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if options_bounds is not None and options_bounds.collidepoint(mx, my):
                    changed_language = run_options(wordle)
                    if changed_language or (config.num_letters != 0 and config.num_letters != len(wordle.word)):
                        prev_lang = wordle.language
                        wordle = re_wordle_api.Wordle()
                        wordle.language = prev_lang
                        wordle.load_language_options()
                        if config.num_letters > 0:
                            wordle.pick_word_from_length(config.num_letters)
                        else:
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

        # Render
        screen.fill((0, 0, 0))
        if time.time() < red_flash_end:
            screen.fill((100, 0, 0))

        # Options button
        options_bounds = plain_text(5,
                                    5,
                                    options_text,
                                    (255, 255, 255),
                                    options_font,
                                    outline=True)

        # Text
        wx = x_for_centering(wordle.word)
        wy = int((letter_height / 5) * 2)
        ind = 0
        for guess in wordle.guesses:
            if guess == "sus" or guess == "amongus" or guess == "amogus" or guess == "impostor":
                screen.blit(pygame.transform.scale(get_amongus(ind / 6), (letter_height, letter_height)),
                            (wx - letter_height, wy))
            ind += 1
            wy += render_word(wordle.generate_response(guess), (wx, wy)) + vertical_spacing
        if len(wordle.guesses) < 6 and (len(wordle.guesses) == 0 or wordle.guesses[-1] != wordle.word):
            render_word(typed_word + " " * (len(wordle.word) - len(typed_word)), (wx, wy))
            render_keyboard(line_1, line_2, line_3, (115, int((vertical_spacing + letter_height) * 6.3076923076923075)))
        else:
            if wordle.guesses[-1] == wordle.word:
                wx = x_for_centering("CONGRATULATIONS!")
                wy += render_word(f"{re_wordle_api.GREEN}CONGRATULATIONS!{re_wordle_api.RESET}",
                                  (wx, wy)) + vertical_spacing
            else:
                if interactable:
                    red_flash_end = time.time() + 2
                wx = x_for_centering("INCORRECT")
                wy += render_word(f"{re_wordle_api.YELLOW}INCORRECT{re_wordle_api.RESET}", (wx, wy)) + vertical_spacing
                wx = x_for_centering("THE WORD WAS")
                wy += render_word(f"{re_wordle_api.WHITE}THE WORD WAS{re_wordle_api.RESET}",
                                  (wx, wy)) + vertical_spacing
                wx = x_for_centering(wordle.word)
                wy += render_word(re_wordle_api.GREEN + wordle.word + re_wordle_api.RESET, (wx, wy)) + vertical_spacing
            interactable = False
        pygame.display.update()
    config.save()
    return play_again


keep_playing = run_game()
while keep_playing:
    keep_playing = run_game()
pygame.quit()
