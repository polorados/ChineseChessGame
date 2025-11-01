class Player:
    def _init_(self, name):
        self.id = id(self)
        self.name=name
        self.pieces=[]

    def add_piece(self, piece):
        if piece not in self.pieces:
            self.pieces.append(piece)

    def remove_piece(self, piece):
        if piece in self.pieces:
            self.pieces.remove(piece)

    def get_alive_pieces(self):
        return [piece for piece in self.pieces if piece.is_alive]
        
    def __str__(self):
        return f"Player({self.name}) with {len(self.get_alive_pieces())} active pieces"

