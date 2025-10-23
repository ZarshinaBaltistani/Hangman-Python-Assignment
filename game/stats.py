import json
from pathlib import Path
stats_file = Path("hangman_game/stats.json")

# For Statistics of the game
def load_statistics():
    if not stats_file.exists():
        return{
            "games_played" : 0,
            "wins" : 0,
            "losses" : 0,
            "total_score": 0,
            "win_rate": 0.0,
            "average_score_per_game": 0.0
        }
    try:
        with open(stats_file, "r") as f:
            return json.load(f)
    except IOError as e:
        print(f"Error loading stats, resetting to default: {e}")
        return load_statistics()
        
#For saving statistics
def save_statistics(stats: dict):
    try:
        with open(stats_file, "w") as f:
            json.dump(stats, f , indent=4)
    except IOError as e:
        print(f"Error saving statistics, {e}")

# Update Statistics
def update_statistics(stats: dict, result: str, score:int):
    stats["games_played"]  += 1
    stats["total_score"] += score
    if result == "win":
        stats["wins"] += 1
    elif result == "loss":
        stats["losses"] += 1
    # Average score per game and win rate 
    if stats["games_played"] > 0:
        stats["win_rate"] = (stats["wins"]) / (stats["games_played"]) * 100
        stats["average_score_per_game"] = (stats["total_score"]) / (stats["games_played"]) 
    return stats

