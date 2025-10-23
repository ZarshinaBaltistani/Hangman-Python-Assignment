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
#Initialize Game State    
    guessed_letters = set()
    wrong_guess = 0
    max_wrong_guess = 6
#Update Log file
    update_log(log_file_path, f"Word: {word_tob_guess} \n ***** Guesses *****")
#Main Game Loop
    while True:
      progress_string  = build_progress_string(word_tob_guess, guessed_letters)
      
      #Call Display Function to Show everthing
      display.game_state(progress = progress_string, guessed_letter = guessed_letters, wrong_count= wrong_guess,
                        Hangman_stages= ascii_art.get_hangman_stage(wrong_guess))
      
      #Check for Win Condition 
      if "_" not in progress_string:
          display.show_win_message(word_tob_guess)
          # Logging and Scoring
          score = score_cal(len(word_tob_guess), wrong_guess)
          display.show_score(score)

          update_log(log_file_path, "--- Result ---")
          update_log(log_file_path, "Result: WIN")
          update_log(log_file_path, f"Score: {score}")
          update_log(log_file_path, f"Wrong Guesses: {wrong_guess}")
          return "win", score
          
      #Check for Loss Condition 
   
      if wrong_guess >= max_wrong_guess:
         display.show_loss_message(word_tob_guess)
         score = 0
         display.show_score(score)
         update_log(log_file_path, "===== Result =====")
         update_log(log_file_path, "Result: Loss")
         update_log(log_file_path, f"Score: {score}")
         update_log(log_file_path, f"Worng Guesses: {wrong_guess}")
         return "loss", score

      #Guess Validation
      guess = display.get_guess()

      #if player already guessed the letter
      if guess in guessed_letters:
          display.repeated_guess(guess)
          # Logging
          update_log(log_file_path, f"Guess: {guess} Repeated!, Try another one")
          time.sleep(1)
          continue
      # If new guess by the user
      guessed_letters.add(guess)
 
      #If guess in correct
      if guess in word_tob_guess:
          display.correct_guess(guess)
          #New Logging
          update_log(log_file_path, f"Guess: {guess} Correct!")
      else:
          display.show_wrong_guess(guess)
          wrong_guess += 1     #Penalty
          #New Logging
          update_log(log_file_path, f"Guess: {guess} (Wrong)")
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
    score = (word_length *10) -(wrong_guess*5)
    return max(0,score)





    