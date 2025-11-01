class Board:
    def __init__(self, piece_list, cell_list):
        self.rows = 9  # Swapped rows and cols
        self.cols = 7
        # Create grid where each position is a tuple (piece, cell)
        self.grid = [[(None, None) for _ in range(self.cols)] for _ in range(self.rows)]
        self.move_history = []
        self.setup_board(piece_list, cell_list)
        

    def setup_board(self, piece_list, cell_list):
        # Initialize all positions with (None, None)
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = (None, None)
        
        # Set pieces
        for row, col, piece in piece_list:
            current_cell = self.grid[row][col][1]  # Preserve existing cell
            self.grid[row][col] = (piece, current_cell)
        
        # Set cells
        for row, col, cell in cell_list:
            current_piece = self.grid[row][col][0]  # Preserve existing piece
            self.grid[row][col] = (current_piece, cell)

    def is_valid_move(self, piece, new_position):

        row, col = new_position
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False  # Out of bounds
        target = self.grid[row][col]
        origin = self.grid[piece.position.row][piece.position.col]
    
        if piece.name != 'TIGER' and piece.name != 'LION':

            if abs(row - piece.position.row) + abs(col - piece.position.col) == 1:
                if target[0] == None and target[1] != 'river':
                    return True
                if target[0] != None and target[0].owner != piece.owner and target[1].type != 'river':
                    if target[0].rank <= piece.rank:
                        return True
                if piece.rank == 1: 
                    if target[0] != None and target[0].owner != piece.owner:
                        if target[0].rank == 8:
                            return True
                     # 
                    if target[1].type == 'river':
                        if target[0] == None:
                            return True
                        elif target[0].name == 'RAT':
                            if target[0].owner != piece.owner:
                                if origin[1].type == 'river':
                                    return True
                                else :
                                    return False
                    if origin[1].type == 'river' and target[1].type != 'river'and target[0] != None:   
                        return False
        else : 
            if abs(row - piece.position.row) + abs(col - piece.position.col) == 1:
                if target[0] == None and target[1] != 'river':
                    return True
                if target[0] != None and target[0].owner != piece.owner and target[1].type != 'river':
                    if target[0].rank <= piece.rank:
                        return True
            elif self.grid[row-1][col][1].type == 'river' and self.grid[piece.position.row+1][piece.position.col].type == 'river':
                if col == piece.position.col:
                    for i in range (piece.position.row+1, row):
                        if self.grid[i][col][0] != None:
                            return False
                    if target[0] == None:
                        return True
                    elif target[0] != None and target[0].owner != piece.owner and target[0].rank <= piece.rank:
                        return True
                    else: 
                        return False
                    
            elif self.grid[row+1][col][1].type == 'river' and self.grid[piece.position.row-1][piece.position.col].type == 'river':
                if col == piece.position.col:
                    for i in range (row+1, piece.position.row):
                        if self.grid[i][col][0] != None:
                            return False
                    if target[0] == None:
                        return True
                    elif target[0] != None and target[0].owner != piece.owner and target[0].rank <= piece.rank:
                        return True
                    else: 
                        return False
            
            elif self.grid[row][col-1][1].type == 'river' and self.grid[piece.position.row][piece.position.col+1].type == 'river':
                if row == piece.position.row:
                    for i in range (piece.position.col+1, col):
                        if self.grid[row][i][0] != None:
                            return False
                    if target[0] == None:
                        return True
                    elif target[0] != None and target[0].owner != piece.owner and target[0].rank <= piece.rank:
                        return True
                    else: 
                        return False
                    
            elif self.grid[row][col+1][1].type == 'river' and self.grid[piece.position.row][piece.position.col-1].type == 'river':
                if row == piece.position.row:
                    for i in range (col+1, piece.position.col):
                        if self.grid[row][i][0] != None:
                            return False
                    if target[0] == None:
                        return True
                    elif target[0] != None and target[0].owner != piece.owner and target[0].rank <= piece.rank:
                        return True
                    else: 
                        return False
            
            

    def update_position(self, piece, new_position):
        row, col = new_position
        target = self.grid[row][col]
        origin = self.grid[piece.position.row][piece.position.col]
        if target[0] != None:
            target[0].is_captured = True
            target = (piece, target[1])
            piece.position = new_position
            origin = (None, origin[1])
        elif target[1].type == 'trap' and target[1].owner != piece.owner:
            piece.is_captured = True
            target = (None, None)
            origin = (None, origin[1])
        elif target[1].type == 'den' and target[1].owner != piece.owner:
            target = (piece, None)
            piece.position = new_position
            origin = (None, origin[1])
        else :
            target = (piece, target[1])
            piece.position = new_position
            origin = (None, origin[1])
        

            