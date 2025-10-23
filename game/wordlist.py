from pathlib import Path
import random
categories_dir = Path("hangman_game/words/categories")

#For Loading words
def load_words():
    word_data= {}
#Check for directory
    if not categories_dir.exists():
        print(f"Error: Categories directory not found at {categories_dir}")
        return {}
# Loop through all the directoires in the categories
    for file_path in categories_dir.glob("*.txt"):
        category_name = file_path.stem
        try:
            with open(file_path, "r") as f:
                words = [line.strip().lower() for line in f if line.strip()]
            if words:
                word_data[category_name] = words   
        except IOError as e:
            print("Error loading the file {file_path}: {e}")
    return word_data                
           
#Selecting Random Word form Categories Slected by User
def get_random_word(word_data: dict, category: str = None):
 if category:
        # User selected a specific category
        if category in word_data:
            return random.choice(word_data[category])
        else:
            print(f"Warning: Category '{category}' not found. Picking from all words.")
            # Fallback to picking from all
    
     # --- Pick from all words ---
 all_words = []
 for word_list in word_data.values():
    all_words.extend(word_list)
        
    if not all_words:
        # This is a critical error, the game can't run
        print("Error: No words were loaded. Cannot pick a random word.")
        return None # Return None to signal an error
 return random.choice(all_words)
        
           
