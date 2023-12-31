#=============================================================================
# Models one of the plastic ships in the Battleship game
# The plastic ships have 2-5 holes in them depending on the size of the ship.
# When a hit is registered, a red peg is placed in the plastic hole.
# 
# The class has the following attributes:
# 
#    type (str) - like "Cruiser"
#    size (int) - 3
#    status (list) - [0, 0, 0] to model the plastic holes that get filled with red pegs
#    loc (int, int) - the row, col location of the ship - ex. (3, 5)
#    horizontal (bool) - boolean if horizontal in orientation - ex. True
# 
#    In the above example, the ship is a "Cruiser" and occupies (3, 5), (3, 6), (3, 7)
#    If it were vertical instead, the ship would occupy (3, 5), (4, 5) and (5, 5)
#
# Methods
#    markHitAt(r, c) - modify the status of the ship to a 'hit' at (r, c) - "fill in the
#                      plastic hole with a red peg"
#    isHitAt(r, c) - is the a "red peg" at (r, c)?
#    isSunk() - the entire ship is sunk - all the status[] are 'hit's (i.e. filled with "red pegs")
#=============================================================================
class Ship:

    #### DO NOT MODIFY LINES BELOW ####
    def __init__(self, type: str, size: int):
        '''
        Constructor
        type - Name of the ship
        size - how many pegs are in the ship
        '''
        self.HitParts = {}
        self.type = type
        self.size = size
        self.status = [0 for _ in range(size)]  # models the plastic pegs marking a 'hit'
        self.loc = (0, 0)                       # default initialization
        self.horizontal = True                  # default initialization

    def getType(self) -> str:
        return self.type

    def getSize(self) -> int:
        return self.size

    # r, c valid numbers are 0 - 9 representing rows A - J and columns 1 - 10
    # Assume that r and c are valid
    def setLocation(self, r: int, c: int):
        self.loc = (r, c)

    def getLocation(self):
        return self.loc

    def setHorizontal(self, h: bool) -> None:
        self.horizontal = h

    def isHorizontal(self) -> bool:
        return self.horizontal
    #### DO NOT MODIFY LINES ABOVE ####
    def __str__(self):
        return self.type
    ### Add the following methods below and any others you may find useful ###
    def GetAbrv(self):# returns the abbreviation
        return self.abrv
    def new(type): # Custom Constructor 
        if not (type in shiptypes):
            return None 
        self = Ship(type,shiptypes[type]["size"])
        self.abrv = shiptypes[type]["abbreviation"]
        self.HitParts = {}
        return self 
    def markHitAt(self, r: int, c: int):
        self.HitParts[str(r)+","+str(c)] = True
    def isSunk(self) -> bool:
        return len(self.HitParts) == self.size

    def isHitAt(self, r: int, c: int) -> bool: # checks if the ship is hit at
        return str(r)+","+str(c) in self.HitParts
shiptypes = { #ship info
    "Submarine" : {
        "size" : 3,
        "abbreviation" : 's',
        "HitScore" : 3,
        "SunkScore" : 5,
        'Disc' : "Has 3 slots",
    },
    "Carrier" : {
        "size" : 5,
        "abbreviation" : 'c',
        "HitScore" : 1,
        "SunkScore" : 8,
        'Disc' : "Has 5 slots",
    },
    "Battleship" : {
        "size" : 4,
        "abbreviation" : 'b',
        "HitScore" : 2,
        "SunkScore" : 6,
        'Disc' : "Has 4 slots",
    },
    "Patrol Boat" : {
        "size" : 2,
        "abbreviation" : 'p',
        "HitScore" : 3,
        "SunkScore" : 4,
        'Disc' : "Has 2 slots",
    },
    "Destroyer" : {
        "size" : 3,
        "abbreviation" : 'd',
        "HitScore" : 3,
        "SunkScore" : 5,
        'Disc' : "Has 3 slots",
    },
}