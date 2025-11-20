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

def convert_indices_to_coordinate(row, col):
    """
    Convert (row, col) indices back to coordinate like 'a1', 'g9', etc.
    Grid: left to right abcdefg, top to bottom 987654321
    Example: row 8, col 0 = 'a1'
    """
    if not (0 <= row <= 8 and 0 <= col <= 6):
        raise ValueError("Row must be 0-8, col must be 0-6")
    
    # Convert column index to letter (0=a, 1=b, 2=c, 3=d, 4=e, 5=f, 6=g)
    letter = chr(ord('a') + col)
    
    # Convert row index to number
    # Top row is row index 0 = 9, bottom row is row index 8 = 1
    # So: 0->9, 1->8, 2->7, 3->6, 4->5, 5->4, 6->3, 7->2, 8->1
    number = 9 - row
    
    return f"{letter}{number}"

def main():
    ui = UserInterface()
    choice = ui.display_welcome2()
    if choice == "quit":
        sys.exit(0)
    if choice == "load":
        filename = ui.prompt_filename_load()
        if filename == 'quit':
            sys.exit(0)
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

        # print(f"New game cell type: {type(game.board.grid[3][0][1][0])}")
        # print(f"New game cell value: {repr(game.board.grid[3][0][1][0])}")
    
    display_board = True
    while True:
        try: 
            if game.recording:
                if display_board:
                    ui.display_board(game.board.grid)
                else:
                    display_board = True
                
                ui.display_game_status(game)

                ui.display_help_playback()

                user_input = ui.get_user_input()

                if user_input == 'next':
                    if game.move_history == []:
                        print("End of playback reached.")
                        time.sleep(0.5)
                        display_board = False
                        continue
                    
                  
                    game.players[game.whose_turn].moved_this_turn = False
                    print(f"Replaying move: {game.move_history[0]}")
                    origin = game.move_history[0][1]
                    destination = game.move_history[0][2]
                    origin_row, origin_col = convert_coordinate(origin)
                    destination_row, destination_col = convert_coordinate(destination)
                    origin_position = Position(origin_row, origin_col)
                    destination_position = Position(destination_row, destination_col)
                    game.move_piece(origin_position, destination_position)
                    game.move_history.pop(0)
                    game.switch_turn()
                    time.sleep(0.5)
                    continue

                if user_input == 'exit':
                    game.recording = False
                    display_board = False
                    choice = ui.display_welcome2()
                    if choice == 'quit':
                        sys.exit(0)
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
                        display_board = True
                    continue

                else : 
                    print("Invalid command")
                    display_board = False
                    continue


                

            else:

                if display_board:
                    ui.display_board(game.board.grid)
                    if game.completed == False:
                        ui.display_game_status(game)
                    else:
                        ui.display_game_result(game.players[game.whose_turn].name)
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
                    if game.completed:
                        print("The game has ended. You cannot perform new moves")
                        time.sleep(0.5)
                        display_board = False
                        continue
                    origin,destination = ui.display_move_prompt(game)
                    origin_row, origin_col = convert_coordinate(origin)
                    destination_row, destination_col = convert_coordinate(destination)

                    origin_position = Position(origin_row, origin_col)
                    destination_position = Position(destination_row, destination_col)
                    result, message = game.move_piece(origin_position,destination_position) 
                    print(message)
                    time.sleep(0.5)
                    if result == True: 
                        mover = game.players[game.whose_turn]
                        # if game.whose_turn == 0:
                        #     mover = game.players[0]
                        # else:
                        #     mover = game.players[0]
                        result1, playerwhowon = game.check_victory(mover,destination_position)
                        if result1 == True:
                            ui.display_game_result(game.players[playerwhowon].name)
                            game.completed = True
                            display_board = False
                            break
                            
                        continue
                    

                    else :
                        display_board = False
                        continue
                    
                if user_input == 'history':
                    ui.display_move_history(game)
                    display_board = False
                    continue

                
                if user_input == 'resign':
                    if game.completed:
                        print("The game has ended. You cannot resign now.")
                        time.sleep(0.5)
                        display_board = False
                        continue
                    if ui.display_resignation(game.players[game.whose_turn].name):
                        print(f"{game.players[game.whose_turn].name} has resigned")
                        game.switch_turn()
                        ui.display_game_result(game.players[game.whose_turn].name)
                        display_board = False
                        game.completed = True
                        continue
                    else:
                        display_board = False
                        continue

                
                if user_input == 'undo':
                    if game.completed:
                        print("The game has ended. You cannot undo moves now.")
                        time.sleep(0.5)
                        display_board = False
                        continue
                    if not game.move_stack:
                        print("No moves to undo.")
                        time.sleep(0.5)
                        display_board = False
                        continue

                    else : 

                        
                        move = game.move_stack.pop()


                        if game.players[move["prev_turn"]].undos <=0:
                            print(f'No undos left for {game.players[move["prev_turn"]].name}.')
                            game.move_stack.append(move)
                            time.sleep(0.5)
                            display_board = False
                            continue
                        else:
                            game.move_stack.append(move)
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
                
                if user_input == 'load':
                    filename = ui.prompt_filename_load()
                    if filename == 'quit':
                        display_board = False
                        continue
                    loaded_game = SaveGame.load_game(filename)
                    if loaded_game is not None:
                        game = loaded_game
                        print(f"Game loaded from {filename}")
                    else:
                        print(f"Failed to load game from {filename}")
                        display_board = False

                    time.sleep(0.5)
                    continue
                
                if user_input == 'record':
                    filename = ui.prompt_filename_record()
                    if filename == 'quit':
                        display_board = False
                        continue
                    SaveGame.save_game(game, filename)
                    print(f"Game recorded to '{filename}'")
                    time.sleep(0.5)
                    display_board = False
                    continue

                if user_input == 'playback':
                    filename = ui.prompt_filename_playback()
                    if filename == 'quit':
                        display_board = False
                        continue
                    playback_game = SaveGame.load_game(filename)
                    if playback_game is not None:
                        game = Game(playback_game.players[0], playback_game.players[1])
                        game.move_history = playback_game.move_history
                        game.recording = True
                        print(f"Game loaded for playback from {filename}")
                    else:
                        print(f"Failed to load game from {filename}")
                        display_board = False
                    time.sleep(0.5)
                    continue
                    





                if user_input == 'save':
                    filename = ui.prompt_filename_save()
                    if filename in ('quit', 'exit', 'q'):
                        display_board = False
                        continue
                    SaveGame.save_game(game, filename)
                    print(f"Game saved to '{filename}'")

                    # loaded_game = SaveGame.load_game(filename)
                    # print(f"Loaded game cell type: {type(loaded_game.board.grid[3][0][1][0])}")
                    # print(f"Loaded game cell value: {repr(loaded_game.board.grid[3][0][1][0])}")

                    time.sleep(0.5)
                    display_board = False
                    continue

                if user_input == 'endturn' or user_input == 'et':
                    if game.completed:
                        print("The game has ended. You cannot end turns now.")
                        time.sleep(0.5)
                        display_board = False
                        continue
                    if not game.players[game.whose_turn].moved_this_turn:
                        print("You must make a move before ending your turn.")
                        time.sleep(0.5)
                        display_board = False
                        continue
                    else:
                        game.switch_turn()
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