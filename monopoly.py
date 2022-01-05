from random import randint

class Player:
    def __init__(self, name):
        self.dobble = 0
        self.money = 1500
        self.hand = []
        self.pos = 0
        self.location = Lcases[0]
        self.jailcount = 0

    def roll(self):
        if self.jailcount == 0:
            dice1 = randint(1, 6)
            dice2 = randint(1, 6)
            rollval = dice1 + dice2
            self.pos += rollval
            if self.pos > 40:
                self.pos += -40
            self.location = Lcases[self.pos]
            self.location.action(self)
        else:
            self.location.action(self)


class Case:
    def __init__(self, name, pos):  # name = str ; pos = int 0<=pos<=40
        self.name = name
        self.pos = pos


class Property(Case):
    def __init__(self, group, price, rentDict):  # group = [Property...] ; price = [priceCase, priceHouse, priceHostel] ; rentDict = dict
        self.houses = 0
        self.group = group
        self.price = price
        self.rentDict = rentDict
        self.owner = None

    def action(self, player):
        if self.owner == None:
            while True:
                try:
                    ans = str(input(f"Do you want to buy {self.name} for {self.price[0]}$ ? ('Y'=yes, 'N'=no)\n"))
                except(ValueError): 'sfojkseopfsjop^f'



class Special(Case):
    func = None
    def __init__(self, action):  # action = function
        self.action = action


Lcases = []

def test(player):
    print('bbbb')

a = Special(test)
print('ertergergedrgerg')