import pickle
import traceback
import time
import os

class SaveGame:
    @staticmethod
    def save_game(game, filename: str = "game.jungle"):
        
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', filename)


        
        try:
            with open(filepath, 'wb') as file:
                pickle.dump(game, file)
            
        except Exception as e:
            print(f"Error saving game: {e}")

    @staticmethod
    def load_game(filename: str = "game.jungle"):
        
        filepath = os.path.join('data', filename)
        try:
            with open(filepath, 'rb') as file:
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
        folder_path = os.path.join('data')
        jungle_files = []
        
        os.makedirs(folder_path, exist_ok=True)
        # Get all files in current directory
        for filename in os.listdir(folder_path):
            full_path = os.path.join(folder_path, filename)
            # Check if file ends with .jungle and is a file (not directory)
            if filename.endswith('.jungle') and os.path.isfile(full_path):
                jungle_files.append(filename)
        
        return jungle_files

    @staticmethod
    def get_jungle_record_files():
        """
        Returns a list of all .record save files in the current directory.
        """
        folder_path = os.path.join('data')
        jungle_files = []
        os.makedirs(folder_path, exist_ok=True)
        # Get all files in current directory
        for filename in os.listdir(folder_path):
            full_path = os.path.join(folder_path, filename)
            # Check if file ends with .jungle and is a file (not directory)
            if filename.endswith('.record') and os.path.isfile(full_path):
                jungle_files.append(filename)
        
        return jungle_files