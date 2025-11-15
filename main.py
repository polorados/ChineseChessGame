from view.userinterface import UserInterface
from model.save_game import SaveGame
from model.game import Game
from model.player import Player
from model.piece import Position
import sys
import time
import traceback


def convert_coordinate(coord):
    """
    Convert coordinate like 'a1', 'g9', etc. to (row, col) indices.
    Grid: left to right abcdefg, top to bottom 987654321
    Example: a1 = row 8, col 0
    """
    if len(coord) != 2:
        raise ValueError("Coordinate must be 2 characters (e.g., 'a1', 'g9')")
    
    letter = coord[0].lower()
    number = coord[1]
    
    # Convert letter to column index (a=0, b=1, c=2, d=3, e=4, f=5, g=6)
    col_index = ord(letter) - ord('a')
    
    # Convert number to row index 
    # Top row is 9 = row index 0, bottom row is 1 = row index 8
    # So: 9->0, 8->1, 7->2, 6->3, 5->4, 4->5, 3->6, 2->7, 1->8
    row_index = 9 - int(number)
    
    return row_index, col_index


def main():
    ui = UserInterface()
    choice = ui.display_welcome2()
    if choice == "load":
        filename = ui.prompt_filename_load()
        game = SaveGame.load_game(filename)

        # print(f"New game cell type: {type(game.board.grid[3][0][1][0])}")
        # print(f"New game cell value: {repr(game.board.grid[3][0][1][0])}")

        if game is None:
            if ui.confirm("Start a new game instead? (y/n):"):
                player1_name, player2_name = ui.get_player_names()
                game = Game(player1_name, player2_name)

            else:
                print("No game to run. Exiting.")
                sys.exit(0)
    else:
        player1_name, player2_name = ui.get_player_names()
        player1 = Player(player1_name)
        player2 = Player(player2_name)
        game = Game(player1, player2)

        print(f"New game cell type: {type(game.board.grid[3][0][1][0])}")
        print(f"New game cell value: {repr(game.board.grid[3][0][1][0])}")
    
    display_board = True
    while True:
        try: 
            if display_board:
                ui.display_board(game.board.grid)
                ui.display_game_status(game)
                ui.display_help()
            if display_board == False:
                display_board = True
            

            
            user_input = ui.get_user_input()
            if user_input == 'help' or user_input == 'h':
                ui.display_help()
                display_board = False
                continue

            if user_input == 'status':
                display_board = True
                continue

            if user_input == 'move' or user_input == 'm':
                origin,destination = ui.display_move_prompt(game)
                origin_row, origin_col = convert_coordinate(origin)
                destination_row, destination_col = convert_coordinate(destination)

                origin_position = Position(origin_row, origin_col)
                destination_position = Position(destination_row, destination_col)
                result, message = game.move_piece(origin_position,destination_position) 
                print(message)
                time.sleep(0.5)
                if result == True: 
                    if game.whose_turn == 0:
                        mover = game.players[1]
                    else:
                        mover = game.players[0]
                    result1, playerwhowon = game.check_victory(mover,destination_position)
                    if result1 == True:
                        ui.display_game_result(game.players[playerwhowon].name)
                        display_board = False
                        break
                        
                    continue
                

                else :
                    display_board = False
                    continue
                
            if user_input == 'history':
                ui.display_move_history(game.move_history)
                display_board = False
                continue

            
            if user_input == 'resign':
                if ui.display_resignation(game.players[game.whose_turn].name):
                    print(f"{game.players[game.whose_turn].name} has resigned")
                    ui.display_game_result(game.players[1 - game.whose_turn].name)
                    display_baord = False
                    break
                else:
                    display_board = False
                    continue

            
            if user_input == 'undo':
                if game.players[1-game.whose_turn].undos <=0:
                    print("No undos left for opponent.")
                    time.sleep(0.5)
                    display_board = False
                    continue
                else:
                    result, message = game.undo_move()
                    print(message)
                    time.sleep(0.5)
                    if result == True:
                        print(f"{game.players[game.whose_turn].name} has used an undo. Remaining undos: {game.players[game.whose_turn].undos-1}")
                        game.players[game.whose_turn].undos -= 1
                        time.sleep(0.5)
                        continue
                    else:
                        display_board = False
                        continue
            
            if user_input == 'save':
                filename = ui.prompt_filename_save()
                SaveGame.save_game(game, filename)
                print(f"Game saved to {filename}")

                # loaded_game = SaveGame.load_game(filename)
                # print(f"Loaded game cell type: {type(loaded_game.board.grid[3][0][1][0])}")
                # print(f"Loaded game cell value: {repr(loaded_game.board.grid[3][0][1][0])}")

                time.sleep(0.5)
                display_board = False
                continue


            
                




            if user_input == 'quit' or user_input == 'q':
                if ui.display_quit_confirmation():
                    print("Thanks for playing!")
                    break

            else : 
                print("Invalid command. Type 'help' or 'h' for a list of commands.")
                display_board = False
                continue

                


        except KeyboardInterrupt:
            if ui.display_quit_confirmation():
                print("Thanks for playing!")
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            if ui.confirm("Continue playing? (y/n): "):
                continue
            else:
                break



    


if __name__ == "__main__":
    main()