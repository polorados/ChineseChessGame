from enum import Enum


class Player(Enum):
    P1 = 1
    P2 = 2
class Rank:
    ELEPHANT = 8
    LION = 7
    TIGER = 6
    LEOPARD = 5
    WOLF = 4
    DOG = 3
    CAT = 2
    RAT = 1
class Position:
    row: int
    col: int
class Piece:
    id: int
    name: str
    rank: Rank
    owner: Player
    position: Position
    is_alive: bool = True

    def __init__(self, name, rank, owner, position):
        self.id = id(self)
        self.name = name
        self.rank = rank
        self.owner = owner
        self.position = position