import pickle
import traceback
import time
import os

class SaveGame:
    @staticmethod
    def save_game(game, filename: str = "game.jungle"):
        
        try:
            with open(filename, 'wb') as file:
                pickle.dump(game, file)
            print(f"Game successfully saved to '{filename}'")
        except Exception as e:
            print(f"Error saving game: {e}")

    @staticmethod
    def load_game(filename: str = "game.jungle"):
        
        try:
            with open(filename, 'rb') as file:
                game = pickle.load(file)
            print(f"Game successfully loaded from '{filename}'")
            time.sleep(0.5)
            return game
        except Exception as e:
            print(f" Error loading game: {e}")
            traceback.print_exc()
            return None
    
    @staticmethod
    def get_jungle_save_files():
        """
        Returns a list of all .jungle save files in the current directory.
        """
        jungle_files = []
        
        # Get all files in current directory
        for filename in os.listdir('.'):
            # Check if file ends with .jungle and is a file (not directory)
            if filename.endswith('.jungle') and os.path.isfile(filename):
                jungle_files.append(filename)
        
        return jungle_files
