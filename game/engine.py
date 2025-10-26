from ui import display
import time
from pathlib import Path
from game import ascii_art
from datetime import datetime
#Comparison Function between True Word and Guessed One
def build_progress_string(word: str, guessed: set) -> str:
    progress_list = []
    for letter in word:
        if letter in guessed:
            progress_list.append(letter)
        else:
            progress_list.append("_")
    return " ".join(progress_list)

# For Play Game
def play_game(word_tob_guess: str, log_file_path: Path):
    
    # Initialize Game State    
    guessed_letters = set()
    wrong_guess = 0
    max_wrong_guess = 6
    
    # Log initialization
    update_log(log_file_path, f"Word: {word_tob_guess} \n ***** Guesses *****")
    
    # Main Game Loop
    while True:
        progress_string  = build_progress_string(word_tob_guess, guessed_letters)
        
        # Call Display Function to Show everything
        display.game_state(
            progress = progress_string, 
            guessed_letter = guessed_letters, 
            wrong_count= wrong_guess,
            Hangman_stages= ascii_art.get_hangman_stage(wrong_guess)
        )
        
        # --- Check for Win Condition (Before taking new input) ---
        if "_" not in progress_string.replace(" ", ""): # Check win condition on continuous word
            display.show_win_message(word_tob_guess)
            # Logging and Scoring
            score = 100 - (wrong_guess * 10) # Simple scoring
            score = max(0, score)
            display.show_score(score)
            update_log(log_file_path, "===== Result =====")
            update_log(log_file_path, "Result: Win")
            update_log(log_file_path, f"Score: {score}")
            update_log(log_file_path, f"Wrong Guesses: {wrong_guess}")
            return "win", score
            
        # --- Check for Loss Condition ---
        if wrong_guess >= max_wrong_guess:
            # Must display the final Hangman stage before the loss message
            display.game_state(
                progress = progress_string, 
                guessed_letter = guessed_letters, 
                wrong_count= wrong_guess,
                Hangman_stages= ascii_art.get_hangman_stage(wrong_guess)
            )
            display.show_loss_message(word_tob_guess)
            score = 0
            display.show_score(score)
            # Logging
            update_log(log_file_path, "===== Result =====")
            update_log(log_file_path, "Result: Loss")
            update_log(log_file_path, f"Score: {score}")
            update_log(log_file_path, f"Wrong Guesses: {wrong_guess}")
            return "loss", score

        # --- Get Guess (Accepts single letter, sequence, or word) ---
        guess_input = display.get_guess(len(word_tob_guess))

        # Check for empty input (e.g., if user interrupts the game)
        if not guess_input:
            continue
        # If the input length matches the word length, treat it as a full word guess
        if len(guess_input) == len(word_tob_guess):
            if guess_input == word_tob_guess:
                # Instant Win
                guessed_letters.update(set(word_tob_guess)) # Reveal all for display
                update_log(log_file_path, f"Full word guess: '{guess_input}' Correct! (Instant Win)")
                continue # Loop will check win condition next
            else:
                # Instant Loss (High-stakes guess)
                display.show_wrong_guess(guess_input)
                wrong_guess = max_wrong_guess # Max out wrong guesses
                update_log(log_file_path, f"Full word guess: '{guess_input}' Incorrect! (Instant Loss)")
                time.sleep(1)
                continue # Loop will check loss condition next
        
        # --- 2. SINGLE LETTER / SEQUENCE GUESS CHECK ---
        
        # Set to track if the current input contained any *new* incorrect letters
        penalty_incurred = False 
        
        # New letters found in the guess input that were not previously guessed
        new_letters_to_check = set(guess_input) - guessed_letters
        
        # If the user only guessed letters they already guessed, inform them and move on
        if not new_letters_to_check:
            display.repeated_guess(guess_input)
            update_log(log_file_path, f"Guess: {guess_input} (No new letters to check)")
            time.sleep(1)
            continue

        # Process the new letters in the sequence/single guess
        # We process all letters in the input and only incur *one* penalty if *any* new letter is wrong.
        newly_revealed_correct_letters = 0
        
        for letter in new_letters_to_check:
            # Add to guessed letters, whether it's right or wrong, 
            # so they don't get penalized twice for the same letter.
            guessed_letters.add(letter) 
            
            if letter in word_tob_guess:
                # Correct letter
                newly_revealed_correct_letters += 1
                update_log(log_file_path, f"Letter: '{letter}' Correct!")
            else:
                # Incorrect letter - only incur penalty once per input, 
                # but log all incorrect letters.
                update_log(log_file_path, f"Letter: '{letter}' Wrong.")
                penalty_incurred = True
        
        # Feedback for the user based on the outcome of the input
        if newly_revealed_correct_letters > 0 and not penalty_incurred:
            # Sequence or single letter was 100% correct
            display.correct_guess(guess_input)
        elif newly_revealed_correct_letters > 0 and penalty_incurred:
            # Sequence had some correct letters but also some incorrect ones
            print(f"-> Mixed result: You revealed {newly_revealed_correct_letters} correct letter(s), but also guessed an incorrect one.")
        
        # Apply the single penalty turn for the whole sequence input if any new letter was wrong
        if penalty_incurred:
            wrong_guess += 1
            # Show a generic wrong guess message for the input
            display.show_wrong_guess(f"Sequence/Letter(s) in '{guess_input}'") 
        
        time.sleep(1)
#Update Log file
def update_log(log_file_path, message: str):
    try:
        with open(log_file_path, "a") as f:
           f.write(f"{message} \n")
    except IOError as e:
        print(f"Error: Could not write to log file {log_file_path}: {e}")

# Score Calculation
def score_cal(word_length: int, wrong_guess: int) -> int:
    score = (word_length *10) - (wrong_guess*5)
    return max(0,score)





    
