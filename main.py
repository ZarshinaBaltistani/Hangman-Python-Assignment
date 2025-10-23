from pathlib import Path
from datetime import datetime
from game import ascii_art, wordlist, engine, stats
from ui import display
import re
#Getting maximum number of games played
def get_mx_game(folder_path: Path):
    max_game = 0
    existing_games = list(folder_path.glob("game*/"))
    for folder in existing_games:
        match_game = re.match(r'game(\d+)', folder.name)
        if match_game:
            num = int(match_game.group(1))
            if num > max_game:
               max_game = num
    return max_game + 1
#log file setting up    
def setup_logging():        
    folder_path = Path("hangman_game/game_log")
    folder_path.mkdir(parents= True, exist_ok=True)
    game_number = get_mx_game(folder_path)
    #New Game Folder Creation
    new_game_folder = Path("hangman_game/game_log")/ f"game{game_number}"
    new_game_folder.mkdir(parents = True, exist_ok= True)

    #Log file creation for the new Game
    log_file_path = new_game_folder / "log.txt"
    with open(log_file_path, "w") as file:
       file.write("Log for Game {game_number} ---\n")
       file.write(f"Timestamp: {datetime.now().strftime("%Y-%M-%D %H:%M:%S")}\n")
    return log_file_path   
def main():
    # Load Statistics
    print("Loading game data, please wait...")
    current_stats = stats.load_statistics()
    
    # Load all words
    word_data = wordlist.load_words()
    if not word_data:
        print("Fatal Error: No word data found. Exiting.")
        return
    # Get the list of categories
    available_categories = list(word_data.keys())
    print("Game loaded successfully!")
    while True:
        # Setup Logging
        log_file_path = setup_logging() 
        # ASK THE USER for their choice
        chosen_category = display.get_category_choice(available_categories)
        # Log the chosen category
        log_category = chosen_category if chosen_category else "All"
        update_log(log_file_path, f"Category: {log_category}")
        # GET THE WORD
        word_tob_guess = wordlist.get_random_word(word_data, chosen_category)
        if not word_tob_guess:
          print("Fatal Error: Could not select a word. Exiting.")
          continue
        #START THE GAME
        print(f"Starting game with a {len(word_tob_guess)}-letter word.")

        # values from engine
        result, score = engine.play_game(word_tob_guess, log_file_path)

        # 8. UPDATE, SAVE, AND DISPLAY STATS
        current_stats = stats.update_statistics(current_stats, result, score)
        stats.save_statistics(current_stats)

        # Log the final stats to the log.txt file 
        update_log(log_file_path, "\n--- Final Statistics ---")
        for key, value in current_stats.items():
          update_log(log_file_path, f"{key.replace('_', ' ').title()}: {value}")

        # Display stats to the user in the console
        display.display_statistics(current_stats)
        # ask to play again ---
        print("Game over. Thanks for playing!")
        if not display.ask_play_again():
            break # Exit the 'while True' loop

# --- You need a log helper function here too ---
def update_log(log_file: Path, message: str):
    """
    Appends a new line of text to the game's log file.
    (This is a helper for main.py)
    """
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{message}\n")
    except IOError as e:
        print(f"Error: Could not write to log file {log_file}: {e}")

if __name__ == "__main__":
 main()        
    
    
