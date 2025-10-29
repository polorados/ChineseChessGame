class Player:
    def _init_(self, name):
        self.name=name
        self.pieces=[ELEPHANT,LION,TIGER,LEOPARD,WOLF,DOG,CAT,RAT]

    def add_piece(self, piece):
        self.pieces.append(piece)

    def remove_piece(self, piece):
        if piece in self.pieces:
            self.pieces.remove(piece)

    def get_piece_at_position(self, position):
        for piece in self.pieces:
             if piece.position.row == position.row and piece.position.col == position.col:
                return piece
        return None

    def get_alive_pieces(self):
        return [piece for piece in self.pieces if piece.is_alive]
