from board import Board
from ship import Ship
from setting import info
import random
'''
The Ocean Board is the portion of the Battleship Unit that holds
ships that the player had placed and keeps track of hits upon each
ship that the opponent has guessed correctly.
'''
class OceanBoard(Board):
 
    def __init__(self, rsize: int, csize: int):
        # call parent's __init__
        # TODO
        super().__init__(rsize,csize)
        self.ships = []
    def MYCanPlaceAt(self,x,y):
        return self.CanPlaceAt(x-1,y-1)
    def CanPlaceAt(self,x,y):
        item = None
        if x <0 or y<0:
            return False
        try:
           item = self.getPiece(x,y)
        except:
            item = False
        return item == None and True or False
    # return False if ship could not be placed at r, c
    #    either r, c are illegal
    #    or ship is too big to be placed there
    #    or another ship is already there
    # Modify 'ship' with the given (r, c) and orientation
    # Add 'ship' to the the OceanBoard's list of 'ships' if placed successfully
    def getShips(self):
        return self.ships
    def MYplaceShip(self, ship: Ship, r: int, c: int, orientation: str): # all methods with my at the start are for my use the ones without my is for computer testing 
        return self.placeShip(ship, r-1, c-1, orientation)
    def placeShip(self, ship: Ship, r: int, c: int, orientation: str) -> bool:
        CanPlace = True
        cx,cy = r,c
        for i in range(ship.getSize()):
            if self.CanPlaceAt(cx,cy):
                if orientation =="h": cy +=1
                else: cx +=1
            else:
                CanPlace = False; break
        if not CanPlace: return False
        cx,cy = r,c
        ship.setLocation(r,c)
        ship.setHorizontal(orientation == 'h')
        for i in range(ship.getSize()):
            self.putPiece(ship,cx,cy)
            #print(cx,cy)
            if orientation =="h": cy +=1
            else: cx +=1
        self.getShips().append(ship)
        return True
    def resetBoard(self):
        self.ships = []
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                self.board[r][c] = None
    # create a board with random units
    def generaterandom(self,settings):
        self.resetBoard()
        ships,shipamt = [],[]
        for name,s in info[settings.getValue("mode")].items():
                ships.append(name)
                shipamt.append(s)
        lx,ly = self.rowSize(),self.colSize()
        while sum(shipamt) != 0 :
            for i,s in enumerate(ships):
                if shipamt[i] == 0: continue
                ship = Ship.new(s)
                rx,ry = random.randrange(1,lx+1),random.randrange(1,ly+1)
                ori = random.randrange(0,2) == 0 and "h" or "y"
                if self.MYplaceShip(ship,rx,ry,ori):
                    shipamt[i] -= 1
                    break

    # are all 'ships' in the OceanBoard sunk?
    def allShipsSunk(self):
        flag = True
        for i in self.ships:
            if not i.isSunk():
                flag = False; break
        return flag
