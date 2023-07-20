from battleshipplayer import BattleshipPlayer
from battleshipplayer import Bot
from ship import Ship
from ship import shiptypes
from display import Display
from setting import Settings as settings
from setting import info
from letter import Letter 
from Error import Errormsg
from  OptionHandler import Options
import time
import os
from ctypes import c_int
import sys,subprocess
import multiprocessing
from art import *# converts ascci
from RemoteHandler import Mysocket as t
Mysocket = t()
import socket
#from keyboard import wait # gets keyboard inputs etc
letters = [*" abcdefghijklmnopqrstuvwxyz"]# creates a list so i can convert a1 ->11
errorhandler = Errormsg() #gets the functions
#score = open('Battleship Project/Score.txt','r')

#Note* All functions with MY.... infront of it was made because the test cases required it to be from 0-9 but the way I coded it was from 1-10 
'''-----Snapshots-----
#1 - Basic function and a bot algorithm works 
#2 - Hard Bot algorithm works and fixed a bug in initplayer
#3 - RemoteHandler Works + prototype Online mode, there is a bug relating to hard bot and numpy not init properly
#4 - Online Mode Works + realised that the webcat submisions for 2 and 3 did not go thru properly because of the size of this file and deleated/edited some libarys to make them smaller
#5 - fixed isempty method bug 
'''




'''
Places the 5 ships onto the Ocean board of 'player'
Creates 5 ships, asks player where it wants them placed, and puts them into
the Ocean board.
'''
'''
playerNumber calls a shot and p1/p2 player units are updated appropriately
return - True if all ships are sunk after the player's shot
'''
errormsg = ""
side = 1
winner = ""
def OnWin(d:Display,winner:BattleshipPlayer,mode,p1 = None,p2 = None): # When Someone wins
    d.clearterminal()
    d.displayUnits(winner,winner.OtherPlayer)
    d.message(str(Letter(text2art(str(winner)+" Wins","small"),"green")))
    WinScreen(d,mode,p1,p2)
def errofunc():# prints errros/system stuff
    global errormsg
    global side
    d = Display()
    if errormsg and errormsg != "": d.message(str(Letter("[System]: "+errormsg,'yellow')),side)
    errormsg = ""
    side = 1
def Myturn(d: Display, p1: BattleshipPlayer, p2: BattleshipPlayer, playerNumber: int) -> bool:
    guesser,nonguesser = playerNumber == 1 and (p1,p2) or (p2,p1)
    guesser.SetOtherPlayer(nonguesser)
    nonguesser.SetOtherPlayer(guesser)
    isOnline = settings.getValue('smod') == 'Online'
    display1 = (p2.CheckIsBot() and not p1.CheckIsBot()) or settings.getValue('smod') == 'Online'
    if display1: playerNumber = 1 # if its plrvsBot only display the plrs board
    done = False
    global errormsg
    global side
    px,py = None,None
    def displayOcean():#displays ocean
        d.clearterminal()
        if display1:
            d.displayUnitsforone(p1,1)
        else:
            d.displayUnits(p1,p2)
        d.newLine()
        errofunc()
    while not done:
        displayOcean()
        you = "You"
        if not guesser.CheckIsBot():
            point = d.ask("{}, which grid are you shooting? ".format(str(guesser)),playerNumber)
            px,py = p1.convertto(point)
            if px == None or py == None: #checks if point is valid
                errormsg = errorhandler.getrandom('OoB').format(point)
                side = playerNumber
                point = None
                continue
            px ,py = px+1,py+1
            if guesser.getTarget().getPiece(px-1,py-1) != None: #checks if point is valid
                errormsg = errorhandler.getrandom('alrshot').format(point)
                side = playerNumber
                point = None
                continue
        else:
            you = str(guesser)
            px,py = guesser.Shoot()
        hit,sunk,hitship = guesser.shootAtOtherPlayer(px,py)
        if guesser.CheckIsBot():#if its a bot then give it its shot data
            guesser.setLastData(lp = (px,py),lht= (sunk and "Sunk") or (hit and "Hit") or "Miss",ship = hit and hitship or None)
        point = letters[px]+str(py)
        string = ""
        if not hit: 
            displayOcean()
            d.message("{}, which grid are you shooting? {}".format(str(guesser),point),playerNumber)
            string = "{} Missed! ".format(you)
        else:
            if not sunk:

                displayOcean()
                d.message("{}, which grid are you shooting? {}".format(str(guesser),point),playerNumber)
                string = "{} Hit {}'s {}! ".format(you,str(nonguesser),str(hitship))
            else:

                displayOcean()
                d.message("{}, which grid are you shooting? {}".format(str(guesser),point),playerNumber)
                string = "{} Sunk {}'s {}! ".format(you,str(nonguesser),str(hitship))
        if not isOnline:
            d.ask(string,playerNumber)
        else:#plan to add smt here
            d.ask(string,playerNumber)
        break
    return px,py,nonguesser.getOcean().allShipsSunk()
def turn(d: Display, p1: BattleshipPlayer, p2: BattleshipPlayer, playerNumber: int) -> bool:
    guesser,nonguesser = playerNumber == 1 and (p1,p2) or (p2,p1)
    Myturn(d,p1,p2,playerNumber)
    global winner
    winner = guesser
    return nonguesser.getOcean().allShipsSunk()
def animate_text(text,d:Display): # does the loading screen thing
  number_of_characters=1
  while not stoptext:
    d.moveTo(8,0)
    d.clearToEndOfLine()
    txt = text[0:number_of_characters]
    d.message(text[0:number_of_characters])
    number_of_characters += 1
    if number_of_characters > len(text):
      number_of_characters = 0
      for i in range(20):
          
        if stoptext: break
        time.sleep(.1)
    time.sleep(0.2)
stoptext = False


def initPlayer(d:Display,plrclass:BattleshipPlayer):
    Done = False
    abv = {}
    nop = str(plrclass) # name of player
    sip = "{}, Choose a ship to place: ".format(nop) #shorten
    global errormsg
    ships,shipamt,disc = [],[],[]
    for name,s in info[settings.getValue("mode")].items():
            ships.append(name)
            shipamt.append(s)
            disc.append(shiptypes[name]["Disc"])
    ships.append("Random")
    shipamt.append(1)
    disc.append("creates a randomly generated board (DOES DELETE ANY PLACED SHIPSd)")
    shipoptions = Options(ships,shipamt,disc)
    def displayOcean():#displays ocean
        d.clearterminal()
        d.displayOcean(plrclass)
        d.message("---Ships---")
        shipoptions.print()
        """
        for name,s in shiptypes.items():
            amt = len([v for v in plrclass.getShipsunit() if v.type == name ])
            abv[s["abbreviation"]] = name
            msg = "{} : {}({})".format(s["abbreviation"],name,s["ammount"]-amt)
            if s["ammount"]-amt == 0:
                msg= str(Letter(msg,"grey"))
            d.message(msg)
            Done = True 
            if s["ammount"]-amt != 0: Done = False;break
        """
        Done = shipoptions.OptionsLeft() == 1
        d.newLine()
        errofunc()
        return Done
    while not Done: #loops selecting ship
        if displayOcean(): break
        letter = d.ask(sip)
        ship,errormsg = shipoptions.GetName(letter.lower())
        if errormsg: 
            errormsg = errorhandler.getrandom(errormsg).format(letter)
            continue
        if ship == "Random":
            plrclass.resetUnit()
            plrclass.getOcean().generaterandom(settings)
            displayOcean()
            break
        point = None
        while True: #loops placing ship
            if not point: # checks for valid point
                displayOcean()
                d.message(sip +ship)
                point = d.ask("Where do you want to place it (ex:a1): ")
            px,py = plrclass.convertto(point)
            if px == None or py == None or not plrclass.CanPlaceAt(px,py): #checks if point is valid
                 errormsg = errorhandler.getrandom('ILLEGAL_Point').format(point)
                 point = None
                 continue
            displayOcean()
            d.message(sip +ship)
            d.message("Where do you want to place it (ex:a1): "+point)
            ori = d.ask("What Orientation do you want (h/v): ")
            ori = ori.replace(" ","")
            if ori.lower() != 'h' and ori.lower() !='v': #checks if ori is valid
                errormsg = "'{}' is not valid option".format(ori)
                continue
            sus = plrclass.MYplaceShip(ship,point,ori.lower()) 
            if not sus:
                point= None
                errormsg = errorhandler.getrandom('ILLEGAL_Place')
            else: break
    d.ask("{} Press [Enter] when ready".format(nop))
    d.clearterminal()
    return plrclass
def playBattleship(d: Display, settings) -> None:
    Basic(d)
def main():
    if 'debugpy' in sys.modules:#checks if it is ran in vsc and if so open in cmd instead
       #Restart()
       pass
    d = Display()
    d.clearterminal()
    settings.setSetting('numplayers', 2)
    LoadingScreen(d)
    HomeScreen(d)
    #playBattleship(d,settings)

#stuff after this is for the home screen stuff
def Basic(d:Display,p1 = None,p2 = None): #basic mode
    settings.setSetting('smod','normal')
    settings.setSetting('mode', 'basic')
    d.clearterminal()
    if not p1:
        p1 = BattleshipPlayer(d.ask("Player 1 enter your name: " ))
    def getP2():
        d.clearterminal()
        errofunc()
        a = d.ask("Player 2 enter your name: " )
        global errormsg
        if a == str(p1): errormsg = "Name already taken"; return getP2()
        return a
    if not p2:
        p2 = BattleshipPlayer(getP2())
    initPlayer(d,p1)
    initPlayer(d,p2)
    wturn = False
    winner:BattleshipPlayer
    while True:
        win = turn(d,p1,p2,int(wturn)+1)
        if win:
            if wturn == 1:
                winner = p2
            else:
                winner = p1
            winner.updateScore(1)
            OnWin(d,winner,Basic,p1,p2)
            break
        wturn = not wturn   
def PlrVsBot(d:Display): #playVSBOT
    global refreshfuncmsg,refreshfuncdata
    Modes = Options(['EasyBot','NormalBot','HardBot','HackerBot','Back'],Info= ["Randomly shoot","Has an algorithm","Uses a better algorithm","Has Hacks but has a 1/3 chance of failing and is dumb"])
    refreshfuncmsg = '--Difficulty--'
    refreshfuncdata= Modes
    name = Modes.GetInput("Choose a difficulty: ",refreshfunc)
    if name == "Back": return Play(d)
    d.clearterminal()
    p1 = BattleshipPlayer(d.ask("Enter your name: " ))
    initPlayer(d,p1)
    p2 = Bot.new(name)(settings)
    wturn = False
    while True:
        win = turn(d,p1,p2,int(wturn)+1)
        if win: OnWin(d,winner,PlrVsBot);print(str(winner) + ' has Won');break
        wturn = not wturn 

def toThread(tochange,server):
    d = Display()
    d.moveTo(1,0)
    d.message(str(Letter("Waiting For A Client To Connect...",'yellow')))
    c,a = server.Host(True)
    a = socket.gethostbyaddr(a[0])
    d.clearterminal()
    tochange.value +=1
    d.message(str(Letter('Client({}) Connected! Press [enter] to continue '.format(a[0]),'green')))
def StartOnlineMoveing(d:Display,k,o,isp):
    player = k
    otherplayer = o
    def Wait(player,otherplayer):
        d.clearterminal()
        d.displayUnitsforone(player)
        d.message("")
        d.message(str(Letter("Waiting For Other Player To Move... ",'yellow')))
        data = Mysocket.WaitForData()
        shotat,isGame= data[0],data[1]
        if isGame: Mysocket.CanDc = False
        px,py = shotat[0],shotat[1]
        point = letters[px]+str(py)
        otherplayer.SetOtherPlayer(player)
        hit,sunk,hitship = otherplayer.shootAtOtherPlayer(px,py)
        d.clearterminal()
        d.displayUnitsforone(player)
        d.message("")
        string = "{} shot at {}".format(str(otherplayer),point)
        if not hit: 
            string+= ' and Missed'
        else:
            if not sunk:
                string+= ' and Hit your '+str(hitship)
            else:
                string+= ' and Sunk your '+str(hitship)
        d.ask(str(Letter(string,'red')))
        if isGame:
            OnWin(d,otherplayer,'Restart')
    def Shoot():
        x,y,IsGame= Myturn(d,player,otherplayer,1)
        Mysocket.sendData([[x,y],IsGame])
        if IsGame:
            Mysocket.CanDc = False
            OnWin(d,player,'Restart')
    if isp == 2:
        Wait(player,otherplayer)
        Shoot()
    else:
        Shoot()
        Wait(player,otherplayer)
    StartOnlineMoveing(d,player,otherplayer,isp)
def Online(d:Display):
    global errormsg
    global refreshfuncmsg,refreshfuncdata
    Modes = Options(['Start Server','Connect to server','Back'])
    refreshfuncmsg = '''Make Sure The Ports and Ip Address(recommended to be set as the host's (person who starts the server) IP) are the same\nyou can change in settings. also make sure the host has started a server\n--Online--'''
    refreshfuncdata= Modes
    name = Modes.GetInput("Choose a Options: ",refreshfunc)
    if name == "Back": return Play(d)
    d.clearterminal()
    settings.setSetting('smod','Online')
    if name == "Start Server":
        '''
        continue_ = multiprocessing.Value('i',0)
        thread = multiprocessing.Process(target = toThread,args = (continue_,Mysocket))
        thread.daemon = True
        thread.start()
        while continue_.value == 0 :
            d.moveTo(2,0)
            a =  d.ask("Input 'restart' to stop: ")'''
        d = Display()
        d.moveTo(1,0)
        d.message(str(Letter("Waiting For A Client To Connect...",'yellow')))
        c,a = Mysocket.Host(True)
        try:
           a= socket.gethostbyaddr(a[0])
        except:
            a = "No Name"
        d.clearterminal()
        d.ask(str(Letter('Client({}) Connected! Press [enter] to continue '.format(a[0]),'green')))
        d.clearterminal()
        player1 = ''
        while True:
            d.clearterminal()
            errofunc()
            player1 = d.ask("What Is Your Name? ")
            if not player1.isspace() and player1 != '':
                player1 = BattleshipPlayer(player1)
                break
            else:
                errormsg = "Invalid Name"
        #initplayer
        Mysocket.sendData(player1)
        player2:BattleshipPlayer
        d.message(str(Letter("Waiting For Client to Input their name...",'yellow')))
        player2 = Mysocket.WaitForData()
        player1.OtherPlayer = player2
        initPlayer(d,player1)
        Mysocket.sendData(player1)
        d.message(str(Letter("Waiting For {} to place their ships...".format(str(player2)),'yellow')))
        player2 = Mysocket.WaitForData()
        StartOnlineMoveing(d,player1,player2,1)
    else:
        d.message(str(Letter("Attempting to connect...",'yellow')))
        if Mysocket.ConnectToHost():
            d.message(str(Letter("Successfully Connected To a Host!",'green')))
            d.message(str(Letter("Waiting For Host to Input their name...",'yellow')))
            player1 = Mysocket.WaitForData()
            player2 = ''
            while True:
                d.clearterminal()
                errofunc()
                player2:str
                player2 = d.ask("What Is Your Name? ")
                if player2 != str(player1) and not player2.isspace() and player2 != '':
                    player2 = BattleshipPlayer(player2)
                    break
                else:
                    errormsg = "Invalid Name"
            Mysocket.sendData(player2)
            d.message(str(Letter("Waiting For {} to place their ships...".format(str(player1)),'yellow')))
            player1 = Mysocket.WaitForData()
            player2.OtherPlayer = player1
            initPlayer(d,player2)
            Mysocket.sendData(player2)
            StartOnlineMoveing(d,player2,player1,2)
        else:
            d.ask(str(Letter("Host Not Found! Press [Enter] to go back ",'red')))
            d.clearterminal()
            Art = text2art("Battle Ship")
            d.message(str(Letter(Art,"blue")))
            Online(d)
        
def BotVsBot(d:Display):#botvsbot
    global refreshfuncmsg,refreshfuncdata
    Modes = Options(['EasyBot','NormalBot','HardBot','HackerBot','Back'],Info= ["Randomly shoot","Has an algorithm","Uses a better algorithm","Has Hacks but has a 1/3 chance of failing and is dumb"])
    refreshfuncmsg = '--Difficulty--'
    refreshfuncdata= Modes
    bt1 = Modes.GetInput("Choose a difficulty for Bot1: ",refreshfunc)
    if bt1 == "Back": return Play(d)
    if bt1 == "HardBot(WIP)": return BotVsBot(d)
    bt2 = Modes.GetInput("Choose a difficulty for Bot2: ",refreshfunc)
    if bt2 == "Back": return Play(d)
    #if bt2 == "HardBot(WIP)": return BotVsBot(d)

    d.clearterminal()
    p1 = Bot.new(bt1)(settings)
    p1.name = "{}1".format(bt1)
    p2 = Bot.new(bt2)(settings)
    p2.name = "{}2".format(bt2)
    wturn = False
    while True:
        win = turn(d,p1,p2,int(wturn)+1)
        if win: OnWin(d,winner,BotVsBot);print(str(winner) + ' has Won');break
        wturn = not wturn   
def WinScreen(d:Display,gamemode,p1 =None,p2 = None):
    if gamemode == 'Restart':
        d.ask("Press [Enter] to restart")
        Restart()
    global refreshfuncmsg,refreshfuncdata
    Modes = Options(['Home','Play Again','Quit'])
    refreshfuncmsg = '--Options--'
    refreshfuncdata= Modes
    def refreshfunc(): #refreshes the loading/home screen
        d = Display()
        d.moveTo(19,0)
        d.clearToEndOfScreen()
        d.moveTo(19,0)
        d.message(str(Letter(refreshfuncmsg,"yellow")))
        refreshfuncdata.print()
        d.newLine()
    name = Modes.GetInput("Choose a option: ",refreshfunc)
    d.home()
    d.clearterminal()
    Art = text2art("Battle Ship")
    d.message(str(Letter(Art,"blue")))
    if name == "Play Again": 
        if p1 and p2 :
            p1.resetUnit()
            p2.resetUnit()
            return gamemode(d,p1,p2)
        else:
            return gamemode(d)
    if name == "Home": return HomeScreen(d)
    elif name =='Quit': 
        d.clearterminal()
        if p1 and p2 :
            winner = p1.score > p2.score and (p1,p2) or (p2,p1)
            winner,loser = winner
            if p1.score == p2.score:
                print("Tie!",p1,':',p1.score,p2,':',p2.score)
            else:
                print(winner,'Won with a score of',winner.score,loser,'Had a score of',loser.score)

def Play(d:Display): #play screen
    global refreshfuncmsg,refreshfuncdata
    Modes = Options(['Basic','PlrVsBot','BotVsBot','Online','Back'])
    refreshfuncmsg = '--Modes--'
    refreshfuncdata= Modes
    name = Modes.GetInput("Choose a mode: ",refreshfunc)
    if name == "Back": return HomeScreen(d)
    func = None
    try: func = globals()[name]
    except: func = Play
    func(d)
refreshfuncmsg = ""
refreshfuncdata = None
def refreshfunc(): #refreshes the loading/home screen 
    d = Display()
    d.moveTo(8,0)
    d.clearToEndOfScreen()
    d.moveTo(8,0)
    d.message(str(Letter(refreshfuncmsg,"yellow")))
    refreshfuncdata.print()
    d.newLine()
def Settings(d:Display):
    n,k = [],[]
    for i,v in settings.getSettings().items():
        if i in settings.MutableSettings:
            n.append(i)
            k.append(v)
    n.append("Back")
    k.append('')
    settingsopts = Options(n,[],k)
    global refreshfuncmsg,refreshfuncdata
    refreshfuncmsg = '--Settings--'
    refreshfuncdata= settingsopts
    name = settingsopts.GetInput("What setting do you want to change: ",refreshfunc)
    if name == "Back": return HomeScreen(d)
    value = d.ask("What do you want to change it to? ")
    settings.setSetting(name,value)
    Settings(d)
def HomeScreen(d:Display):
    Homeop = Options(['Play',"Settings"])
    global refreshfuncmsg,refreshfuncdata
    refreshfuncmsg = '--Home--'
    refreshfuncdata= Homeop
    name = Homeop.GetInput("Where Do you want to go (ex: a,b,c,d): ",refreshfunc)
    func = None
    try: func = globals()[name]
    except: func = HomeScreen
    func(d)
def LoadingScreen(d:Display):#loading screen
    Art = text2art("Battle Ship")
    d.message(str(Letter(Art,"blue")))
    d.message('[TIP]: It is recommended to play in fullscreen')
    d.message('[TIP]: You Can Type "restart" at anytime to restart the game')
    d.ask(str(Letter("Press [Enter] to start ","yellow")))
    '''global stoptext
    thread = Thread(target=animate_text,args= (str(Letter("Press [Enter] to start ","yellow")),d))
    thread.start()
    wait("enter")
    stoptext = True
    thread.join()'''
    d.moveTo(8,0)
    d.clearToEndOfScreen()
def SocketDC():
    d= Display()
    d.clearterminal()
    Art = text2art("Sorry")
    d.message(str(Letter(Art,"red")))
    d.message(str(Letter('your enemy has disconnected, press [enter] to restart ',"red")))
    d.ask('')
    Restart()
def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])
def Restart(): #there is a but with restart
    open_file(__file__)
    try:
        os._exit(0)
    except:
        sys.exit()
if __name__ == "__main__":
    main()
    #SocketDC(Display())

    