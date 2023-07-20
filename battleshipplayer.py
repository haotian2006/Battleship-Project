import imp
from oceanboard import OceanBoard
from targetboard import TargetBoard
from letter import Letter
from ship import Ship
from ship import shiptypes
import math
import random
np = None
from setting import Settings as settings
try:
    import numpy as np #try to import numpy
except:
    np = None
class BattleshipPlayer:
 
    '''
    Models the Battleship Player
      player = Battleship("Joe")    # default 10x10 board

    State Variables
      name (str) - the name of the player
      score (int) - the score of the player
      ocean (OceanBoard) - the board which contains all of the ships
      target (TargetBoard) - the board whih contains all the shots made
    '''
                             # optional parameters default is 10x10
    def __init__(self, name: str, rsize=10, csize=10):
        self.name = name
        self.score = 0
        self.Moves = 0
        self.ocean = OceanBoard(rsize, csize)
        self.target = TargetBoard(rsize, csize)

    def getName(self) -> str:
        return self.name

    def getOcean(self) -> OceanBoard:
        return self.ocean

    def getTarget(self) -> TargetBoard:
        return self.target

    def getScore(self) -> int:
        return self.score
    def SetOtherPlayer(self,other):
        self.OtherPlayer = other 
    ### DO NOT MODIFY ABOVE METHODS ###

    #### MODIFY BELOW ####
    ### Add the following methods below and any others you may find useful ###

    '''
    loc: grid location like 'a1' or 'j10'
    orientation: 'h' or 'v' for horizontal or vertical
    return: True if ship was successfully placed
    '''
    def GetShips(self):
        return self.getOcean().getShips()
    def __str__(self):
        return self.getName()
    def convertto(self,loc):#converts a1 to 1,1
        x,y = "",""
        for s in loc.replace(" ", ""):
            try:
                y += str(int(s))
            except:
                x += s.lower()
        y = y != "" and int(y) or None
        x = x != "" and (x in letters and letters.index(x)) or None
        try:
            x -=1
            y -=1
            self.getOcean().getPiece(int(x),int(y))
        except:
            return None,None
        return x,y
    def CheckIsBot(self):
        bot = None
        try: bot = self.IsBot
        except: bot = None
        return bot
    def CanPlaceAt(self,x,y):
        return self.getOcean().CanPlaceAt(x,y)
    def getShipsunit(self):
        return self.getOcean().getShips()
    def MYplaceShip(self,ship,loc,orientation):
        px,py = self.convertto(loc)
        px +=1
        py +=1
        conditions = { # simple condition check instead of if statements 
            "Not A Ship Type": not Ship.new(ship),
            "Coords are not valid" : (not px or not py),
            "Not a valid orientation" : (orientation != "h" and orientation != "v")
        }
        for i,v in conditions.items():
            if v: return False
        return self.getOcean().MYplaceShip(Ship.new(ship),px,py,orientation)
    def placeShip(self, ship: Ship, loc: str, orientation: str) -> bool:
        px,py = self.convertto(loc)
        conditions = { # simple condition check instead of if statements 
            "Not A Ship Type": not Ship,
            "Coords are not valid" : (not px or not py),
            "Not a valid orientation" : (orientation != "h" and orientation != "v")
        }
        for errormsg,v in conditions.items():
            if v: return False
        return self.getOcean().placeShip(ship,px,py,orientation)
        """
        CanPlace = True
        cx,cy = px,py
        for i in range(ship.getSize()):
            if self.CanPlaceAt(cx,cy):
                if orientation =="h": cy +=1
                else: cx +=1
            else:
                CanPlace = False; break
        if not CanPlace: return False
        shipb = self.getShips()
        cx,cy = px,py
        for i in range(ship.getSize()):
            shipb.putPiece(ship,cx-1,cy-1)
            if orientation =="h": cy +=1
            else: cx +=1
        self.getShipsunit().append(ship)
        return True,""
        """

    '''
    Process the shot at (r, c) and return (hit, sunk, name)
      - Determine if there is a hit
      - Check if the ship is sunk
      - Get the name of the ship (if there is a hit)
      - Mark the ship as being hit
    '''
    def allShipsSunk(self):
        return self.ocean.allShipsSunk()
    def shootAtOtherPlayer(self,px,py): 
        self.Moves +=1
        hitship:Ship
        hitship = self.OtherPlayer.getOcean().getPiece(px-1,py-1)
        hit,sunk,name = None,None,None
        if not hitship: 
            self.getTarget().MYmarkMiss(px,py)
        else:
            name = hitship
            hit = True
            hs,ss = shiptypes[str(hitship)]["HitScore"],shiptypes[str(hitship)]["SunkScore"]
            self.getTarget().MYmarkHit(px,py)
            hitship.markHitAt(px-1,py-1)
            if settings.getValue('smod') != 'normal':
                if not hitship.isSunk():
                    self.updateScore(hs)
                else:
                    sunk= True
                    self.updateScore(ss)
        return hit,sunk,name
    def shotAt(self, r: int, c: int) -> bool:
        hitship:Ship
        hitship = self.getOcean().getPiece(r,c)
        hit,sunk,name = False,False,''
        if hitship:
            hit = True
            self.target.markHit(r,c)
            name = str(hitship)
            hitship.markHitAt(r,c)
            if hitship.isSunk():
               sunk = True
        else:
            self.target.markMiss(r,c)
        return hit,sunk,name
    def shipAt(self,r,c):
        return self.getOcean().getPiece(r,c)
    def getTargetat(self,x,y):
        lx,ly = self.ocean.rowSize(),self.ocean.colSize()
        if x == 0 or y == 0 or x == lx+1 or y == ly +1 : return False
        t = False
        try: t = self.getTarget().getPiece(x-1,y-1)
        except: t= False
        return t
    def markTargetHit(self, r: int, c: int) -> None:
        self.getTarget().markHit(r,c)

    def markTargetMiss(self, r: int, c: int) -> None:
        self.getTarget().markMiss(r,c)

    '''
    Resets both the ocean and target board so that game could
    be restarted
    '''
    def resetUnit(self) -> None:
        self.getOcean().resetBoard()
        self.getTarget().resetBoard()
        self.Moves = 0
    '''
    Adds num to the score
    '''
    def updateScore(self, num: int) -> None:
        self.score += num
letters = [*" abcdefghijklmnopqrstuvwxyz"]
class Bot(BattleshipPlayer): #an ai class to 1v1 
    def __init__(self, name: str, rsize=10, csize=10,settings = None):
        super().__init__(name,rsize,csize)
        self.settings = settings
        self.IsBot = True
        self.CreateRandBoard()
        self.LastPos = None
        self.LastHitType = None
        self.hittables = {}
    def ShootAtRandom(self):# gets a rand pos from the board
        lx,ly = self.ocean.rowSize(),self.ocean.colSize()
        while True:
            px,py = random.randrange(1,lx+1),random.randrange(1,ly+1)
            if self.getTarget().getPiece(px-1,py-1) == None: #checks if point is valid
                return px,py
    def setLastData(self,lp = None,lht= None,ship = None): # sets the last data (for bots)
        if ship:
            self.hittables['{},{}'.format(lp[0],lp[1])] = ship
        self.LastPos = lp or self.LastPos
        self.LastHitType = lht or self.LastHitType
    def CreateRandBoard(self):
        self.ocean.generaterandom(self.settings)
    def GetRandDir(self):# return a random direaction
        x,y = 0,0
        if random.randrange(0,2) == 0:
            x = random.randrange(0,2)
            x = x==0 and -1 or x
        else:
            y = random.randrange(0,2)
            y = y==0 and -1 or y
        return x,y
    def Splitstr(self,string:str): #splits a 1,1 to 1 1
        slist = string.split(',')
        return int(slist[0]),int(slist[1])
    def Hunt(self): #hunts for a ship
        target,first,second= None,None,None
        for pos,ships in self.hittables.items():
            if not ships.isSunk() and not target:
                target,first = ships,pos; continue# gets a ship
            if target and target == ships:
                second = pos; break # gets another ship in  a diffrent pos thats ref. the same one 
        if not target: return self.ShootAtRandom()
        fx,fy = self.Splitstr(first)
        if not second: 
            sx,sy = self.GetPosClose(fx,fy)
            return sx,sy # if not a second hit for the ship then get a near by pos
        sx,sy = self.Splitstr(second)
        row = 'y'
        if sx == fx: row = "x"
        #input("{},{}||{},{}||,{},{}".format(letters[fx],fy,letters[sx],sy,row,1))
        dir = random.randrange(0,4) == 0 and -1 or 1
        attempt1 = False
        while True:
            if row == "x":
                 sy += 1*dir
            else: sx += 1*dir
            hittype = self.getTargetat(sx,sy)
            if hittype == None:
                return sx,sy
            elif hittype == "Miss" or hittype == False:
                dir = dir == -1 and 1 or -1
                if attempt1: return self.ShootAtRandom() # if dir dose't match
                attempt1 = True
    def GetPosClose(self,px,py): #gets random side of the given position 
        while True:
            ex,ey = px,py
            dx,dy = self.GetRandDir()
            ex +=dx; ey +=dy
            if self.getTargetat(ex,ey) == None: #checks if point is valid
                return ex,ey
    def new(dif):# gets 
        return globals()[dif]
class EasyBot(Bot):# will just guess 
    def __init__(self,settings):
        super().__init__("EasyBot",settings= settings)
    def Shoot(self):
       return self.ShootAtRandom()
class HardBot(Bot):#generates a heatmap and uses the size of the ships to predict shots 
    def __init__(self,settings):
        if not np:
            raise Exception('you have to install numpy to use hardbot')
        super().__init__("HardBot",settings= settings)
    def generateHeatMap(self):# creates a heat map with some algorithm I found online 
        #https://towardsdatascience.com/coding-an-intelligent-battleship-agent-bf0064a4b319
        prob_map = np.zeros([10, 10])
        ship:Ship
        shotmap = np.zeros([10,10])
        for i,v in enumerate(self.getTarget().board):
            for _i,_v in enumerate(v):
                shotmap[i][_i] = int(_v == None and "0" or '1')#inserts the data from targetboard to shotmap
        for ship in self.OtherPlayer.GetShips():
            size = shiptypes[ship.type]["size"] - 1
            for row in range(10):
                for col in range(10):
                    if self.getTarget().getPiece(row,col) == None:
                        endpoints = []
                        if row - size >= 0:
                            endpoints.append(((row - size, col), (row + 1, col + 1)))
                        if row + size <= 9:
                            endpoints.append(((row, col), (row + size + 1, col + 1)))
                        if col - size >= 0:
                            endpoints.append(((row, col - size), (row + 1, col + 1)))
                        if col + size <= 9:
                            endpoints.append(((row, col), (row + 1, col + size + 1)))
                        for (start_row, start_col), (end_row, end_col) in endpoints:
                            if np.all(shotmap[start_row:end_row, start_col:end_col] == 0):
                                prob_map[start_row:end_row, start_col:end_col] += 1
                    
                    if self.getTarget().getPiece(row,col) != None and \
                            self.OtherPlayer.getOcean().getPiece(row,col) != None and \
                            not self.OtherPlayer.getOcean().getPiece(row,col).isSunk():  

                        if (row + 1 <= 9) and (self.getTarget().getPiece(row+1,col) == None):
                            if (row - 1 >= 0) and \
                                    (self.OtherPlayer.getOcean().getPiece(row-1,col) != None and
                                     not self.OtherPlayer.getOcean().getPiece(row-1,col).isSunk() )and \
                                    (self.getTarget().getPiece(row-1,col) == "Hit"):
                                prob_map[row + 1][col] += 15
                            else:
                                prob_map[row + 1][col] += 10

                        if (row - 1 >= 0) and (self.getTarget().getPiece(row-1,col) == None):
                            if (row + 1 <= 9) and \
                                    (self.OtherPlayer.getOcean().getPiece(row+1,col) != None and
                                     not self.OtherPlayer.getOcean().getPiece(row+1,col).isSunk() )and \
                                    (self.getTarget().getPiece(row+1,col) == "Hit"):
                                prob_map[row - 1][col] += 15
                            else:
                                prob_map[row - 1][col] += 10

                        if (col + 1 <= 9) and (self.getTarget().getPiece(row,col+1) == None):
                            if (col - 1 >= 0) and \
                                    (self.OtherPlayer.getOcean().getPiece(row,col-1) != None and
                                     not self.OtherPlayer.getOcean().getPiece(row,col-1).isSunk() )and \
                                    (self.getTarget().getPiece(row,col-1) == "Hit"):
                                prob_map[row][col + 1] += 15
                            else:
                                prob_map[row][col + 1] += 10

                        if (col - 1 >= 0) and (self.getTarget().getPiece(row,col-1) == None):
                            if (col + 1 <= 9) and \
                                    (self.OtherPlayer.getOcean().getPiece(row,col+1) != None and
                                     not self.OtherPlayer.getOcean().getPiece(row,col+1).isSunk() )and \
                                    (self.getTarget().getPiece(row,col+1) == "Hit"):
                                prob_map[row][col - 1] += 15
                            else:
                                prob_map[row][col - 1] += 10
                    elif self.getTarget().getPiece(row,col) == "Miss":
                        prob_map[row][col] = 0
                              
        self.Pmap =  prob_map 
    def Shoot(self):
        return self.guess_prob()
    def guess_prob(self):
        self.generateHeatMap()
        max_indices = np.where(self.Pmap == np.amax(self.Pmap))#sorts the heatmap
        guess_row, guess_col = max_indices[0][0]+1, max_indices[1][0]+1
        return guess_row, guess_col
class NormalBot(Bot):# combination of guessing and logic 
    def __init__(self,settings):
        super().__init__("NormalBot",settings= settings)

    def Shoot(self):
        return self.Hunt()
class HackerBot(Bot):# can see where you stuff is placed in
    def __init__(self,settings):
        super().__init__("HackerBot",settings= settings)
    def Shoot(self):
        #has a 1/3 chance of missing 
        if random.randrange(0,2) == 0: return self.ShootAtRandom()
        lx,ly = self.ocean.rowSize(),self.ocean.colSize()
        while True:
            for i,v in enumerate(self.OtherPlayer.ocean.board):
                for _i,_v in enumerate(v):
                    if _v and  self.getTarget().getPiece(i,_i) == None:
                        return i+1,_i+1