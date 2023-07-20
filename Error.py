import math,random
class Errormsg(): # allows me to get a random error message
    errors = {
        'OoB':[#out of bounds
            "Out of bounds '{}'",
            "You can't shoot there '{}'",
            "You can't shoot there '{}', Try Again",
            "Sorry but you can't shoot there '{}'",
            "Why? Try Again '{}'",
            "You realise that is out of bounds right???? '{}'"
        ],
        'alrshot' : [
            "You already shot at '{}'",
            "You can't shoot there '{}'",
            "You can't shoot there, theres a mark there '{}'",
            "You can't shoot there, look at your Target Board again '{}'",
            "Try again you can't shoot there '{}'",
            "Try again you already shot there '{}'"
        ],
        'ILLEGAL_Point' : [
            "ILLEGAL placement '{}'",
            "ILLEGAL placement '{}', Try Again"
        ],
        'ILLEGAL_Place' : [
            "ILLEGAL placement! Try Again ",
        ],
        "Na" :[
            "Not A Valid Option '{}'",
        ],
        'Ne': [
            "No More ({}) Options",
        ]
    }
    def getrandom(self,error):
        return self.errors[error][random.randrange(0,len(self.errors[error]))]