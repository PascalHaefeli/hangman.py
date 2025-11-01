import random
import platform

def welcome():
    print("=========================================================================================================================")
    print("")
    print("Welcome to hangman.py, the non-graphical hangman-game for Linux terminals!")
    print("You need to guess a random word picked from your system's dictionary at [/usr/share/dict/words].")
    print("You can guess the word letter by letter by inputting basic latin letters one at a time into the terminal when prompted.")
    print("Once you have guessed all the letters, you win! But if you input incorrect letters 10 times, it's game over for you!")
    print("Time to play!")
    print("")
    print("=========================================================================================================================")

def check_os():
    if platform.system() == "Linux":
        try: 
            dict_file = "/usr/share/dict/words"
            return dict_file
        except:
            print("If you're not on a Debian-based system, you might need to install a dictionary to /usr/share/dict/words for this game to work.")
            quit()
    elif platform.system() == "Windows":
        print("Just install Linux, please...")
        print("Anyway, this game only works on Linux.")
        quit()
    elif platform.system() == "Darwin":
        print("A Mac? Why not Linux? It's free!")
        print("Anyway, this game only works on Linux.")
        quit()
    else:
        print("I am not recognizing this OS. Are you using a phone?")
        print("Anyway, this game only works on Linux.")
        quit()
    

def get_random_word():
    dict_file = check_os()
    with open(dict_file, "r") as file:      #"with" keyword releases system ressources after access
        text = file.read()
        text = text.split()
        word = random.choice(text)
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
