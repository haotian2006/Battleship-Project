from battleshipplayer import BattleshipPlayer
from letter import Letter
import os
from platform   import system as system_name  # Returns the system/OS name
from subprocess import call   as system_call  # Execute a shell command
import sys
def clear_screen():
    """
    Clears the terminal screen.
    """
    #taken from stack overflow and modified  
    # Clear screen command as function of OS
    command = 'cls' if system_name().lower().startswith('win') else 'clear'

    # Action
    if command == 'cls':
        os.system("cls")
    else:
        system_call([command])
'''
Display - a class that handles the display of the Battleship game. It handles
all the printing and inputing for the game. It has some methods that help
move the cursor around for a more pleasant user game experience.
'''
class Display:

    #### DO NOT MODIFY LINES BELOW ####
    # move to 1, 1
    def home(self) -> None:
        print(u'\u001b[H', end='')

    # move cursor to line, col
    def moveTo(self, line, col) -> None:
        print(u'\u001b[' + f"{line};{col}H", end='')

    # move cursor to column col 
    def moveToColumn(self, col) -> None:
        print(u'\u001b[' + f"{col}G", end='')

    # clear to the end of line (keeping cursor at the current position)
    def clearToEndOfLine(self) -> None:
        print(u'\u001b[K', end='')

    # clear to the end of screen (keeping cursor at the current position)
    def clearToEndOfScreen(self) -> None:
        print(u'\u001b[J', end='')

    # clear screen and move to top left (1,1) of screen
    def clearScreen(self) -> None:
        self.home()
        self.clearToEndOfScreen()

    # return the proper column position for player X
    def playerColumn(self, playerNum: int) -> str:
        if playerNum== 2:
            column = 76
        else:
            column = 0
        return column

    # display message for player X
    def message(self, msg: str, playerNum = 1) -> None:
        self.moveToColumn(self.playerColumn(playerNum))
        print(msg)

    # ask for input from player X
    def ask(self, msg: str, playerNum = 1) -> str:
        self.moveToColumn(self.playerColumn(playerNum))
        d= None
        try:
            d = input(msg)
        except: sys.exit()# this is added because of a bug with the restart function in game.py 
        if d == 'restart': 
            from game import Restart
            Restart()
            #self.clearterminal()
            #LoadingScreen(self)
        return d

    def newLine(self):
        print()
    #### DO NOT MODIFY LINES ABOVE ####

    #### MODIFY BELOW ####
    def clearterminal(self): # fully clears terminal
        clear_screen()
    # display the Ocean board of the player
    def displayOcean(self,plr:BattleshipPlayer,print = True) -> None:
        self.message(Letter(plr.getName()+"'s Battleship Unit","bold"))
        self.message(Letter("  Ocean","blue"))
        ships = plr.getOcean()
        bx,by = ships.rowSize(),ships.colSize()
        water = Letter('.', 'blue')
        row = [[' ',*[" "+str(x) for x in range(1,bx+1)] ]]
        for i in range(1 ,by+1):
            row.insert(i,str(Letter(letters[i],"bold"))+" "+(" ").join([i != None and str(Letter(i.GetAbrv().upper(),"yellow")) or str(water) for i in (ships.board)[i-1]]))
        if not print: return row # returns the list for displayunitsfor one to use
        for v in row:
            self.message(str(Letter("".join(v),"bold")))
    # creates a list to be combined with display ocean
    def createtargets(self,plr:BattleshipPlayer) -> list:
        targets = plr.getTarget()
        bx,by = targets.rowSize(),targets.colSize()
        water = Letter('.', 'blue')
        row = [[' ',*[" "+str(x) for x in range(1,bx+1)] ]]
        xMark = str(Letter('x',"red"))
        oMark = str(Letter('o',"bold"))
        for i in range(1 ,by+1):
            row.insert(i,str(Letter(letters[i],"bold"))+" "+(" ").join(
                [(i == "Hit" and xMark) or (i == "Miss" and oMark) or  str(water) for i in (targets.board)[i-1]]))
        return row
    # display one players ocean & target units
    def displayUnitsforone(self,plr:BattleshipPlayer,side = 1) -> None:
        if side == 2:
            self.moveTo(0,0)
        tb = plr.getTarget()
        targets = self.createtargets(plr)
        self.message(plr.getName()+"'s Battleship Unit [Score: {}][Moves: {}] {}[Score: {}]".format(plr.getScore(),plr.Moves,str(plr.OtherPlayer),plr.OtherPlayer.getScore()),side)
        self.message(str(Letter("  Ocean","blue"))+" "*17+str(Letter("  Target","red")),side)
        ships = plr.getOcean()
        bx,by = ships.rowSize(),ships.colSize()
        water = Letter('.', 'blue')
        row = [[' ',*[" "+str(x) for x in range(1,bx+1)] ]+ ["  "]+[' ',*[" "+str(x) for x in range(1,bx+1)] ] ]
        for pi in range(1 ,by+1):
            row.insert(pi,str(Letter(letters[pi],"bold"))+" "+(" ").join(#combines ocean and target lists
            [i != None and (  str(Letter(i.GetAbrv().upper(),i.isHitAt(pi-1,p) and "red" or 'yellow'))) 
            or str(water) for p,i in enumerate((ships.board)[pi-1])])+"   "#adds a space to create target board
            +("").join(targets[pi])
            )
            
        for v in row:
            self.message(str(Letter("".join(v),"bold")),side)
    # display both player 1 and player 2 ocean & target units
    def displayUnits(self, p1, p2) -> None:
        self.clearScreen()
        self.displayUnitsforone(p1,1)
        self.displayUnitsforone(p2,2)
letters = [*" abcdefghijklmnopqrstuvwxyz"]