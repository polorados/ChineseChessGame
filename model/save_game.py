import pickle
import traceback
import time

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
