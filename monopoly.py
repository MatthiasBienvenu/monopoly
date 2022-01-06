from random import randint


class Player:
    def __init__(self, name):
        self.dobble = 0
        self.balance = 1500
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
        if self.owner is None:
            # !!! choice
            if player.balance >= self.price[0]:
                while True:
                    try:
                        ans = str(input(f"What do you want to do with {self.name}? ('b'=buy, 'a'=auction, 'n'=nothing)"))
                        assert ans in ['a', 'n', 's']
                        if ans == 'b':
                            player.balance -= self.price[0]
                            self.owner = player
                            player.hand.append(self)
                        elif ans == 'a':
                            pass
                            # !!! auction
                        break
                    except AssertionError:
                        print('wrong input')
            else:
                while True:
                    try:
                        ans = str(input(f"What do you want to do with {self.name}? ('a'=auction, 'n'=nothing)"))
                        assert ans in ['a', 'n']
                        if ans == 'a':
                            pass
                            # !!! auction
                        break
                    except AssertionError:
                        print('wrong input')
        else:
            # !!! faillite
            price = self.rentDict[self.houses]
            player.balance -= price
            self.owner.balance += price



class Special:
    def __init__(self, name, pos, action):  # name = str ; pos = int 0<=pos<=40 ; action = function
        self.name = name
        self.pos = pos
        self.action = action


a = Property('name', 0, [], [4000], {})

Lcases = [a]

p = Player('player')

a.action(p)