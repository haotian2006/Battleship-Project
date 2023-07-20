from board import Board

#=============================================================================
# Battleship Target Board - this is the vertical board in the Battleship
# game that tracks hits and misses. In the game, when the player guesses and
# hits, a red peg is placed at the coordinate. If it misses, a white peg
# is placed at the coordinate.
# 
# Methods
#    markHit(r, c) - place a "red peg" at (r, c)
#    markMiss(r, c) - place a "white peg" at (r, c)
#    isHit(r, c) - is there a a "red peg" at (r, c)?
#    isEmpty(r, c) - is there any peg at (r, c)?
#=============================================================================
class TargetBoard(Board):

    def __init__(self, rsize: int, csize: int):
        # just call the parent's __init__
        # TODO
        super().__init__(rsize,csize)

    # place a "red peg" at (r, c)
    def MYmarkHit(self,r,c):
        self.markHit(r-1,c-1)
    def markHit(self, r: int, c: int) -> None:
        self.putPiece("Hit",r,c)
        

    # place a "white peg" at (r, c)
    def MYmarkMiss(self,r,c):# made this because my version uses 1-10 not 0-9
        self.markMiss(r-1,c-1)
    def markMiss(self, r: int, c: int) -> None:
        self.putPiece("Miss",r,c)

    # is there a "red peg" (a hit) at (r, c)?
    def MYisHit(self,r,c):
        return self.isHit(r-1,c-1)
    def isHit(self, r: int, c: int) -> bool:
        return self.getPiece(r,c) == "Hit"

    # is there a any peg at (r, c)?
    def MYisEmpty(self,r,c):
        return self.isEmpty(r-1,c-1)
    def isEmpty(self, r: int, c: int) -> bool:
        peiceat =self.getPiece(r,c)
        return (not peiceat)

    