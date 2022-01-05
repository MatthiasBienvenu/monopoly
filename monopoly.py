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
                self.pos -= 40
            self.location = Lcases[self.pos]
            self.location.action(self)
        else:
            self.location.action(self)


class Property:
    def __init__(self, name, pos, group, price, rentDict):  # name = str ; pos = int 0<=pos<=40 ; group = [Property...] ; price = [priceCase, priceHouse, priceHostel] ; rentDict = dict
        self.name = name
        self.pos = pos
        self.houses = 0
        self.group = group
        self.price = price
        self.rentDict = rentDict
        self.owner = None

    def action(self, player):
        if self.owner == None:
            while True:
                try:
                    ans = str(input(f"Do you want to buy {self.name} for {self.price[0]}$ ? ('y'=yes, 'n'=no)\n"))
                    assert ans == 'y' or ans == 'n'
                    if ans == 'y':
                        player.money -= self.price[0]
                        self.owner = player
                        player.hand.append(self)
                    break
                except(ValueError, AssertionError):
                    print("You have to type 'y' or 'n'")


class Special:
    def __init__(self, name, pos, action):  # name = str ; pos = int 0<=pos<=40 ; action = function
        self.name = name
        self.pos = pos
        self.action = action


a = Property('name', 0, [], [400], {})

Lcases = [a]

p = Player('player')

def test(player):
    print('bbbb')

