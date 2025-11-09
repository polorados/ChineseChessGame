from model.game import Game
from model.player import Player
from view.userinterface import UserInterface
from controller.game_controller import GameController

def main():
    
    ui = UserInterface()
    ui.display_welcome()

    
    player1 = Player("White")
    player2 = Player("Black")

    
    game = Game(player1, player2)
    game.initial_board_setup()

    
    controller = GameController(game, ui)
    controller.run()

if __name__ == "__main__":
    main()