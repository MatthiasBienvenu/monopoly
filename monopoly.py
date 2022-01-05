class Player:
    def __init__(self, name):
        self.dobble = 0
        self.money = 1500
        self.hand = []
        self.pos = 0


class Case:
    def __init__(self, name, typ, pos):  # name = str ; typ = 'PROPERTY' or 'SPECIAL' ; pos = int 0<=pos<=40
        self.name = name
        self.typ = typ
        self.pos = pos


class Property(Case):
    def __init__(self, group, price, rentDict):  # group = [Property...] ; price = [priceCase, priceHouse, priceHostel] ; rentDict = dict
        self.houses = 0
        self.group = group
        self.price = price
        self.rentDict = rentDict


class Special(Case):
    def __init__(self, action):  # action = function
        self.action = action