# Problem Set 2, hangman.py
# Name: Skorodenko Dmytro
# Collaborators:
# Time spent: 4 days

# Hangman Game
import random
import string
from enum import Enum

WORDLIST_FILENAME = "words.txt"
INITIAL_GUESSES = 6
ININITAL_WARNINGS = 3
INITIAL_HINT_ATTEMPTS = 1

class BaseVariables():
    """
    This class creates an object with base variables.
    It also has constants inside of it.
    """
    VOWELS = {"a","e","i","o","u"}
    HINT_SYMBOL = "*"
    UNREVEALED_LETTER = "_"
    def __init__(self, secret_word, type_of_game):
        self.guesses_remaining = INITIAL_GUESSES
        self.warnings_remaining = ININITAL_WARNINGS
        self.letters_guessed = set()
        self.secret_word = secret_word
        self.type_of_game = type_of_game
        self.wordlist = wordlist
        self.hint_attempts = INITIAL_HINT_ATTEMPTS


class ValidationResultType(Enum):
    """
    Enum class with different values that
    depend on whehter the guess is valid.
    """
    NOT_LATIN = 1
    LENGTH_RESTRICTION = 2
    GUESS_GUESSED = 3
    VALID_GUESS = 0


class TypeOfGame(Enum):
    """
    Enum class for changing game mode with/without hints.
    """
    HANGMAN_WITH_HINTS = 1
    HANGMAN_WITHOUT_HINTS = 0


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


wordlist = load_words()
BaseVariables.word_list = wordlist


def is_word_guessed(secret_word, letters_guessed):
    """
    This function checks whether the word is guessed.
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: set of letters which has been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """
    if letters_guessed.issuperset(set(secret_word)):
        return True
    return False


def get_guessed_word(secret_word, letters_guessed):
    """
    This function returns word with underscore symbols.
    secret_word: string, the word the user is guessing
    letters_guessed: set of letters which has been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    """
    # getting set of all letters that were not guessed
    check = set(secret_word).difference(letters_guessed)
    new_word = []
    for letter in secret_word:
        if letter in check:
            new_word.append(BaseVariables.UNREVEALED_LETTER + " ")
        else:   
            new_word.append(letter)
    return "".join(new_word).strip()


def get_available_letters(letters_guessed):
    """
    This function returns string of available letters.
    letters_guessed: set of letters which has been guessed so far
    returns: string (of letters), comprised of letters that represents which letters has not
             yet been guessed.
    """
    def get_unique(x):
        nonlocal letters_guessed
        if x in letters_guessed:
            return False
        return True
    # Removing guessed letters from alphabet 
    available_letters = list(filter(get_unique, string.ascii_lowercase))      
    return "".join(available_letters)


def guess_check(guess, letters_guessed):
    """
    This function checks whether the guess is valid.
    guess: string, input from user
    letters_guessed: set of letters which has been guessed so far
    returns: Enum class ValidationResultType; 
    """
    if not guess.isascii() or not guess.isalpha():
        return ValidationResultType.NOT_LATIN
    guess = guess.lower()
    if len(guess) > 1:
        return ValidationResultType.LENGTH_RESTRICTION
    if guess in letters_guessed:
        return ValidationResultType.GUESS_GUESSED 
    return ValidationResultType.VALID_GUESS
    

def guess_try(guess, variables):
    """
    This function checks whether the guess contains in secret word.
    guess: string, input from user
    variables: object of BaseVariables class
    returns: text output depending on guess,
             variables
    """
    variables.letters_guessed.add(guess)
    if guess in variables.secret_word:
        print("Good guess:",
              get_guessed_word(variables.secret_word,
                               variables.letters_guessed))
    else:
        # if letter is vowel -2 guesses
        if guess in BaseVariables.VOWELS:
            variables.guesses_remaining -= 2
        # if letter is not vowel -1 guess
        else:
            variables.guesses_remaining -= 1
        print("Oops! That letter is not in my word:",
              get_guessed_word(variables.secret_word,
                               variables.letters_guessed))
    return variables 


def match_with_gaps(my_word, other_word, letters_guessed):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    variables: object of BaseVariables class
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    """
    if len(my_word) == len(other_word):
        for i in range(len(my_word)):
            if my_word[i] == BaseVariables.UNREVEALED_LETTER:
                if other_word[i] in letters_guessed:
                    return False
                continue
            elif my_word[i] != other_word[i]:
                return False
        else:
            return True


def show_possible_matches(variables, my_word):
    """
    This function prints out possible word matches.
    my_word: string with _ characters, current guess of secret word
    variables: object of BaseVariables class
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    """
    res = []
    my_word = my_word.replace(" ", "")
    for word in BaseVariables.word_list:
        if match_with_gaps(my_word, word, variables.letters_guessed):
            res.append(word)
    if res:
        if len(res) > 30:
            res = random.choices(res, k=30)
        print("Possible word matches are:\n" + " ".join(res))
    else: 
        print("No matches found.")


def display(output, variables):
    """
    This function is created to display data with various print functions.
    output: Enum class with in value, option to triger particular text output.
    variables: object of BaseVariables class
    returns: variables object.
    """
    if output == ValidationResultType.NOT_LATIN:
        print("Oops! That is not a valid character.")
    if output == ValidationResultType.LENGTH_RESTRICTION:
        print("Oops! You can't guess more than 1 character at once.")
    if output == ValidationResultType.GUESS_GUESSED:
        print("Oops! You've already guessed that letter.")
    if variables.warnings_remaining <= 0:
        variables.guesses_remaining -= 1
        print(
              "You have no warnings left so you lose one guess: " +
               get_guessed_word(variables.secret_word,
                               variables.letters_guessed))
        return variables
    print(
         f"You have {variables.warnings_remaining} warnings left: " +
         get_guessed_word(variables.secret_word,
                               variables.letters_guessed))
    return variables


def game_start(variables):
    """
    This function starts the game.
    variables: object of BaseVariables class
    returns: bool, True if user won the game,
                   False otherwise 
    """
    while variables.guesses_remaining > 0:
        if is_word_guessed(variables.secret_word, variables.letters_guessed):
            return True
        hangman_combined(variables)
        print("-----------")
    else:
        return False

def game_result(res, variables):
    """
    This function displays the result of the game.
    res: bool, True if the game was successful
               Fales if the game was unsuccessful
    variables: object of BaseVariables class
    returns: nothing
    """
    if res:
        print(
              "Congratulations, you won!\n" +
              "Your total score for this game is: " +
              f"{variables.guesses_remaining * len(set(variables.secret_word))}"
             )
    else:
        print(f"Sorry, you ran out of guesses. The word was {variables.secret_word}.")


def game_restart():
    """
    This function asks the user whether he/she wants
    to restart the game.
    returns: stop(string)
    """
    valid = False
    while not valid:
        stop = input("Do you want to quit the game. y/n ")
        if stop not in {"y", "n"}:
            print("Please enter y/n.")
        else:
            valid = True
    if stop == "n":
        print()
    return stop


def type_of_game_input():
    """
    This function accepts input from user (integer).
    returns: Enum with int values, option for game.
    """
    valid = False
    while not valid:
        type_of_game = input(
                         "Enter 1, if you want to play hangman with hints\n" +
                         "Enter 0, if you want to play hangman without hints\n" +
                         ">>>> "
                            )
        if type_of_game not in {"1", "0"}:
            print("You should enter 1 or 0.")
            continue
        else:
            if type_of_game == "1":
                type_of_game = TypeOfGame.HANGMAN_WITH_HINTS
                valid = True
            else:
                type_of_game = TypeOfGame.HANGMAN_WITHOUT_HINTS
                valid = True 
    return type_of_game


def game():
    """
    This function starts the game.
    """
    stop = "n"
    while stop != "y":
        secret_word = choose_word(wordlist)
        print("Welcome to the game Hangman!")
        print(f"I am thinking of a word that is {len(secret_word)} letters long.")
        type_of_game = type_of_game_input()
        variables = BaseVariables(secret_word, type_of_game)
        result = game_start(variables)
        game_result(result, variables)
        stop = game_restart()


def hangman_combined(variables): 
    """
    Hangman combined with Hangman with hints.
    variables: object of BaseVariables class.
    Starts up an interactive game of Hangman.
    returns: variables object 
    """
    print(f"You have {variables.guesses_remaining} guesses left.")
    print("Available letters:", get_available_letters(variables.letters_guessed))
    # Used strip in case that user accidently inputs space
    guess = input("Please guess a letter: ").strip()
    if guess == BaseVariables.HINT_SYMBOL and\
                variables.type_of_game == TypeOfGame.HANGMAN_WITH_HINTS:
        show_possible_matches(variables, 
                              get_guessed_word(variables.secret_word,
                                               variables.letters_guessed))
        print(get_guessed_word(variables.secret_word,
                               variables.letters_guessed))
        return variables
    elif guess == BaseVariables.HINT_SYMBOL and variables.hint_attempts > 0:
        print("You play hangman without hints.")
        variables.hint_attempts -= 1
        return variables

    output = guess_check(guess, variables.letters_guessed)
    if output.value > 0:
        variables.warnings_remaining -= 1
        variables = display(output, variables)
        return variables
    guess = guess.lower()
    variables = guess_try(guess, variables)
    return variables



if __name__ == "__main__":
    game()