from unidecode import unidecode
import random
from colorama import Fore
from language_packs import language_pack


def select_language() -> str:
    language_options = language_pack.get("language_options")
    options = str()
    ids = list()
    for option in language_options:
        options += f"\n{option.get('id')}. {option.get('description')}"
        ids.append(option.get("id"))
    while True:
        print(options)
        language = input(f"\n{language_pack.get('language_input')}")
        try:
            language = int(language)
            if language not in ids:
                print(f"{Fore.RED}{language_pack.get('en').get('valid_option_warning')}{Fore.RESET}")
                continue
            for option in language_options:
                if option.get("id") == language:
                    return option.get("name")
        except ValueError:
            print(f"{Fore.RED}{language_pack.get('en').get('number_option_warning')}{Fore.RESET}")


def select_game_mode(language: str = "en") -> str:
    language_info = language_pack.get(language)
    game_modes = language_info.get("game_mode_options")
    options = str()
    ids = list()
    for option in game_modes:
        options += f"\n{option.get('id')}. {option.get('description')}"
        ids.append(option.get("id"))
    while True:
        print(f"\n> {language_info.get('title')}! <\n{options}")
        game_mode = input(f"\n{language_info.get('game_mode_input')}")
        try:
            game_mode = int(game_mode)
            if game_mode not in ids:
                print(f"{Fore.RED}{language_info.get('valid_option_warning')}{Fore.RESET}")
                continue
            for mode in game_modes:
                if mode.get("id") == game_mode:
                    return mode.get("name")
        except ValueError:
            print(f"{Fore.RED}{language_info.get('number_option_warning')}{Fore.RESET}")


def game(language: str = "en", word: str = None, lives: int = 5):
    language_info = language_pack.get(language)
    if word is None:
        print(f"{Fore.RED}{language_info.get('no_words_warning')}{Fore.RESET}")
    hidden_word = ["_" for _ in word]
    while lives > 0:
        letter_hit = False
        print(f"\n{' '.join(hidden_word)} ({len(hidden_word)} {language_info.get('letters')})")
        letter = input(f"({lives} {language_info.get('remaining_guesses')}) {language_info.get('letter')}").lower()
        if len(letter) != 1 or not letter.isalpha():
            print(f"{Fore.RED}{language_info.get('enter_a_single_letter_warning')}{Fore.RESET}")
            continue
        for i in range(len(word)):
            if letter == unidecode(word[i]).lower():
                hidden_word[i] = word[i]
                letter_hit = True
        if "".join(hidden_word) == word:
            print(f"\n'{word}'. {language_info.get('winning_message')}")
            break
        if letter_hit == False:
            lives -= 1
        if lives == 0:
            print(f"\n{language_info.get('losing_message')}.\n{language_info.get('word_reveal_message')} '{word}'.")


def main():
    LIVES = 5
    words = list()
    break_line = "\n=================================================="
    language = select_language()
    print(break_line)
    game_mode = select_game_mode(language)
    print(break_line)
    with open(f"{language}_{game_mode}_words.csv", "r") as file:
        for line in file:
            words.append(line.strip())
    game(language, random.choice(words), LIVES)


if __name__ == "__main__":
    main()
