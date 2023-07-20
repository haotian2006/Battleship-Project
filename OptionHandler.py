from letter import Letter
from display import Display
letters = [*" abcdefghijklmnopqrstuvwxyz"]
#simple class I made to display options for smt
class Options():
    def __init__(self,options:list,amt:list = [],Info = []):
        self.options = options
        self.amt:list = amt
        self.info = Info
    def print(self): # prints out the options 
        rows = []
        for i,v in enumerate(self.options,1):
            amt = None
            try: amt = self.amt[i-1]
            except: amt = None
            info = None
            try: info = self.info[i-1]
            except: info = None
            mystr = "{} : {}".format(letters[i],v)
            if amt != None:
                mystr += '({})'.format(amt)
            if amt == 0:
                mystr = str(Letter(mystr,'grey'))
            if info != None:
                mystr += ' - '+str(info)
            rows.append(mystr)
        for v in rows:
            Display().message(v)
    def GetInput(self,text = "",func = None): # asks for an input 
        a = True
        while a:
            if func: func()
            d = Display().ask(text)
            op,error = self.GetName(d)
            if op: a = False; return op
    def getAmtfromindex(self,i): 
        amt = None
        try: amt = self.amt[i]
        except: amt = None
        return amt
    def OptionsLeft(self):
        amt = 0
        for i in self.amt:
            if type(i) == int and i != 0:
                amt+=1
        return amt
    def NoMoreOpt(self) -> bool:#checks if the player ran out of choices
        flag = True
        for i in self.amt:
            if type(i) == int and i != 0:
                flag = False; break
        return flag
    def GetName(self,v = ""): # gets the name from input
        if not v: return None, "Na"
        v = v.lower()
        index = None
        try: index = letters.index(v)
        except: index = None
        if not index or index-1 > len(self.options)-1 : return None,"Na"
        op = self.options[index-1]
        amt = self.getAmtfromindex(index-1)
        if amt ==0:
            return None,"Ne"
        elif amt:
            self.amt[index-1] -=1
        return op,None
        
    def UpdateAmt(self,newamt):
        self.amt = newamt
    
