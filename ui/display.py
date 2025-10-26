from game import ascii_art
# Ask User To select Category of Word
def get_category_choice(categories: list) -> str:
    print("\nWelcome to Hangman!")
    print("Please choose a category:")
    for i, category in enumerate(categories):
        print(f"{i +1}.{category.capitalize()}")
    #print(f"{len(category)}")
    while True:
        try:
            choice = input(f"Enter you choice  (1 - {len(categories)}):").strip()
            if choice == str(len(categories)) or choice == "":
                print("Please enter a number corresponding to a category.")
                continue
            choice_num = int(choice)

            # Check if the number is in the valid range
            if 1 <= choice_num <= len(categories):
                chosen_category = categories[choice_num - 1] 
                print(f"You selected: {chosen_category.capitalize()}")
                return chosen_category 
            else:
                print("Invalid number. Please try again.")
                
        except ValueError:
            print("Invalid input. Please enter a number.")


def game_state(progress: str, guessed_letter: set, wrong_count: int, Hangman_stages: str):
    print("*"*40)
    print(Hangman_stages)
    print(f"\nWord: {progress}")
    guessed_letter = ",".join(sorted(list(guessed_letter))) if guessed_letter else None
    print(f"Guessed letters: {guessed_letter}")
    print("Remaining attempts: ", 6 - wrong_count)
    print("*"*40)

#Get Guess from User
def get_guess(word_length: int) -> str:
    """
    Prompts the user for a guess (single letter, sequence, or full word).
    Input must be a valid string of letters.
    """
    while True:
        try:
            prompt_text = (
                f"Enter your guess (1 letter, sequence, or {word_length}-letter word): "
            )
            guess_input = input(prompt_text).strip().lower()

            if not guess_input:
                print("Input cannot be empty. Please enter a guess.")
                continue
            
            # Check if input contains only letters
            if not guess_input.isalpha():
                print("Invalid input. Your guess must contain only letters (a-z).")
                continue

            return guess_input
            
        except EOFError:
            # Handle user interrupting the input
            print("\nGame interrupted. Exiting.")
            return ""

#For Repeated Guess
def repeated_guess(letter: str):
    print(f"Sorry You have already guessesed the letter {letter}, Please Guess another letter\n")

#For correct Guess
def correct_guess(letter: str):
    print(f"Correct guess! \n {letter} is in the word")

# For WIn message
def win_message(word: str):
    print("\n*** You Win ***\n")
    print(f"The word was {word}")

# For lose message
def show_loss_message(word: str):
    print(f"\n--- You Lose! ---")
    print(f"The word was: {word}")       

#For Wrong Guess
def show_wrong_guess(letter: str):
    print(f"-> Wrong! '{letter}' is not in the word.")

def show_score(score: int):
    """Displays the score for the round."""
    print(f"\nPoints earned this round: {score}")

def display_statistics(stats: dict):
    print("\n--- All-Time Statistics ---")
    print(f"Games Played: {stats['games_played']}")
    print(f"Wins:         {stats['wins']}")
    print(f"Losses:       {stats['losses']}")
    print(f"Total Score:  {stats['total_score']}")
    print(f"Win Rate:     {stats['win_rate']:.2f}%") # .2f formats to 2 decimal places
    print(f"Avg. Score:   {stats['average_score_per_game']:.2f}")
    print("-----------------------------\n")
    
# In ui/display.py

# ... (all your other display functions) ...

def ask_play_again() -> bool:
    """
    Asks the user if they want to play again.
    Returns True for 'y', False for 'n'.
    """
    while True:
        choice = input("Do you want to play again? (y/n): ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")    