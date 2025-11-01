import random
import requests

def welcome():
    print("=========================================================================================================================")
    print("")
    print("Welcome to hangman.py, the non-graphical hangman-game for terminals!")
    print("You need to guess a random word picked from the first chapter of Mary Shelley's 'Frankenstein'.")
    print("Here's the link: https://www.gutenberg.org/files/84/84-h/84-h.htm#chap01")
    print("You can guess the word letter by letter by inputting basic latin letters one at a time into the terminal when prompted.")
    print("Once you have guessed all the letters, you win! But if you input incorrect letters 10 times, it's game over for you!")
    print("Time to play!")
    print("")
    print("=========================================================================================================================")

def get_random_word():
    response = requests.get("https://www.gutenberg.org/files/84/84-h/84-h.htm#chap01")
    text = response.text.split()
    word = random.choice(text)
    if not word[-1].isalpha():
        word = word[:-1]
    while len(word) < 6:
        word = random.choice(text)
    #print(f"Random word: {word}")      #For cheating and debugging
    return word

def format_word(word):
    word = word.lower()
    if word[-2] == "'":
        word = word[:-2]
    characters = ""
    for char in word:
        characters += char + " "
    return characters
    
def create_underscores(word):
    index = 0
    underscores = ""
    while index < len(word):
        if word[index] == " ":
            underscores += " "
        else:
            underscores += "-"
        index += 1
    return underscores

def create_separator(word):
    index = 0
    separator = ""
    while index < len(word):
        separator += "="
        index += 1
    return separator

def print_messages(underscores, separator, hidden_word, guesses, uncovered, attempts_left):
    print("")
    print(separator)
    print("")
    print(hidden_word)
    print(underscores)
    print("")
    print(f"Letters not contained in the word: {guesses}")
    print(f"Letters you have guessed correctly: {uncovered}")
    print(f"Attempts left: {attempts_left}")
    print("")
    print(separator)

def user_input(guesses, uncovered):
    print("")
    current_letter = input("Please enter a letter: ").lower()
    if len(current_letter) != 1:
        print("Your input is too long! You may only enter one letter at a time!")
        return False
    elif current_letter in guesses or current_letter in uncovered:
        print("You already tried this letter!")
        return False
    elif not current_letter.isalpha():
        print("Your input was not a letter! Only basic latin letters are allowed!")
        return False
    else:
        return current_letter

def unhide_letters(word, uncovered):
    correct_letters = 0
    hidden_word = ""
    for char in word:
        if char in uncovered:
            hidden_word += (char)
            correct_letters += 1
            if correct_letters == len(word) // 2:            #Victory Condition! Had to len(word) // 2 because spaces double the amount of chars in format_word()
                print(f"Congrats! You guessed the word: {word}")
                quit()
        elif char == " ":
            hidden_word += " "
        else:
            hidden_word += "#"
    return hidden_word

def resume_game():
    print("")
    input("Press 'Enter' to continue!")
    print("")
            
def game_loop(word, hidden_word, guesses, uncovered, attempts_left, underscores, separator):
    print_messages(underscores, separator, hidden_word, guesses, uncovered, attempts_left)
    current_letter = user_input(guesses, uncovered)
    if current_letter == False:
        print("")
        resume_game()
        print("")
        game_loop(word, hidden_word, guesses, uncovered, attempts_left, underscores, separator)
    if current_letter in word:
        uncovered.append(current_letter)
        print("The word contains your letter!")
        hidden_word = unhide_letters(word, uncovered)
        print("")
        resume_game()
        print("")
        game_loop(word, hidden_word, guesses, uncovered, attempts_left, underscores, separator)
    else:
        guesses.append(current_letter)
        attempts_left -= 1
        print("")
        print(f"There is no '{current_letter}' in the word!")
        if attempts_left <= 0:
            print("You left the poor guy hanging!")
            print(f"The word was '{word}'.")
            print(separator)
            print("Game Over!")
            quit()
        else:
            print("")
            print("Try again!")
            resume_game()
            print("")
            game_loop(word, hidden_word, guesses, uncovered, attempts_left, underscores, separator)

def main():
    word = format_word(get_random_word())
    underscores = create_underscores(word)
    separator = create_separator(word)
    guesses = []
    uncovered = []
    hidden_word = ""
    for char in word:
        if char != " ":
            hidden_word += "#"
        else:
            hidden_word += " "
    attempts_left = 10
    welcome()
    game_loop(word, hidden_word, guesses, uncovered, attempts_left, underscores, separator)

main()