# MONOPOLY VERSION USA
from random import randint


class Player:
    def __init__(self, name):
        self.dobble = 0
        self.balance = 1500
        self.hand = []
        self.pos = 0
        self.location = Lcases[0]
        self.jailcount = 0

    def roll(self, dice1=randint(1, 6), dice2=randint(1, 6)):
        if self.jailcount == 0:
            rollval = dice1 + dice2
            self.pos += rollval
            if self.pos >= 40:
                self.balance += 200
                self.pos -= 40
            self.location = Lcases[self.pos]
            self.location.action(self)
        else:
            self.location.action(self)
        if dice1 == dice2:
            self.dobble += 1
            if self.dobble == 3:
                self.dobble = 0
                go_to_jail(self)
                return
                # !!! jail
            self.roll()
        else:
            self.dobble = 0


class Box:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos


class Property(Box):
    def __init__(self, name, pos, group, price, rentDict):
        # name = str ; pos = int 0<=pos<=40 ; group = [Property...] ; price = [priceCase, priceHouse] ;
        # rentDict = dict
        super().__init__(name, pos)
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
                        ans = str(input(f"What do you want to do with {self.name}? (0=nothing, 1=auction, 2=buy)"))
                        assert ans in range(3)
                        if ans == 1:
                            player.balance -= self.price[0]
                            self.owner = player
                            player.hand.append(self)
                        elif ans == 2:
                            pass
                            # !!! auction
                        break
                    except AssertionError:
                        print('wrong input')
            else:
                while True:
                    try:
                        ans = str(input(f"What do you want to do with {self.name}? (0=nothing, 1=auction)"))
                        assert ans in range(2)
                        if ans == 1:
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


class Special(Box):
    def __init__(self, name, pos, action):  # name = str ; pos = int 0<=pos<=40 ; action = function
        super().__init__(name, pos)
        self.action = action


# ----- functions for special boxes -----

def go(player):
    pass


def chance(player):
    card = Lchance[0]
    card(player)
    del (Lchance[0])
    Lchance.append(card)


def community_chest(player):
    card = Lcomchest[0]
    card(player)
    del (Lcomchest[0])
    Lcomchest.append(card)


def go_to_jail(player):
    player.pos = 10
    player.location = Lcases[10]
    player.jailcount = 1


fees = 0


def tax100(player):
    global fees
    player.balance -= 100  # !!! faillite
    fees += 100


def tax200(player):
    global fees
    player.balance -= 200  # !!! faillite
    fees += 200


def free_parking(player):
    global fees
    player.balance += fees
    fees = 0


def jail(player):
    if player.jailcount != 0:
        dice1 = randint(1, 6)
        dice2 = randint(1, 6)
        if dice1 == dice2:
            player.roll(dice1, dice2)
        if player.jailcount == 3:
            player.balance -= 50
            player.roll()
            # !!! faillite
        else:
            player.jailcount += 1


# ----- functions for chance cards -----
...
Lchance = []

# ----- functions for community chest cards -----
...
Lcomchest = []

# ----- List of the boxes -----


GO = Special('GO', 0, go)

# prop = Property('name', 0, [], [4000], {})


brown = []
skyblue = []
pink = []
orange = []
red = []
yellow = []
green = []
darkblue = []

MEDITERRANEAN_AVENUE = Property('MEDITERRANEAN_AVENUE', 1, brown, [60, 50], {0: 2, 1: 10, 2: 30, 3: 90, 4: 160, 5: 250})
BALTIC_AVENUE = Property('BALTIC_AVENUE', 1, brown, [60, 50], {0: 4, 1: 20, 2: 60, 3: 180, 4: 320, 5: 450})
ORIENTAL_AVENUE = Property('ORIENTAL_AVENUE', 1, skyblue, [100, 50], {0: 6, 1: 30, 2: 90, 3: 270, 4: 400, 5: 550})
VERMONT_AVENUE = Property('VERMONT_AVENUE', 1, skyblue, [100, 50], {0: 6, 1: 30, 2: 90, 3: 270, 4: 400, 5: 550})
CONNECTICUT_AVENUE = Property('CONNECTICUT_AVENUE', 1, skyblue, [120, 50], {0: 8, 1: 40, 2: 100, 3: 300, 4: 450, 5: 600})
ST_CHARLES_PLACE = Property('ST_CHARLES_PLACE', 1, pink, [140, 100], {0: 10, 1: 50, 2: 150, 3: 450, 4: 625, 5: 750})
STATES_AVENUE = Property('STATES_AVENUE', 1, pink, [140, 100], {0: 10, 1: 50, 2: 150, 3: 450, 4: 625, 5: 750})
VIRGINIA_AVENUE = Property('VIRGINIA_AVENUE', 1, pink, [160, 100], {0: 12, 1: 60, 2: 180, 3: 500, 4: 700, 5: 900})
ST_JAMES_PLACE = Property('ST_JAMES_PLACE', 1, orange, [180, 100], {0: 14, 1: 70, 2: 200, 3: 550, 4: 700, 5: 900})
TENNESSEE_AVENUE = Property('TENNESSEE_AVENUE', 1, orange, [180, 100],{0: 14, 1: 70, 2: 200, 3: 550, 4: 700, 5: 950})  # 950 vs 900 ???
NEW_YORK_AVENUE = Property('NEW_YORK_AVENUE', 1, orange, [200, 100], {0: 16, 1: 80, 2: 220, 3: 600, 4: 800, 5: 1000})
KENTUCKY_AVENUE = Property('KENTUCKY_AVENUE', 1, red, [220, 150], {0: 18, 1: 90, 2: 250, 3: 700, 4: 875, 5: 1050})
INDIANA_AVENUE = Property('INDIANA_AVENUE', 1, red, [220, 150], {0: 18, 1: 90, 2: 250, 3: 700, 4: 875, 5: 1050})
ILLINOIS_AVENUE = Property('ILLINOIS_AVENUE', 1, red, [240, 150], {0: 20, 1: 100, 2: 300, 3: 750, 4: 925, 5: 1100})
ATLANTIC_AVENUE = Property('ATLANTIC_AVENUE', 1, yellow, [260, 150], {0: 22, 1: 110, 2: 330, 3: 800, 4: 975, 5: 1150})
VENTNOR_AVENUE = Property('VENTNOR_AVENUE', 1, yellow, [260, 150], {0: 22, 1: 110, 2: 330, 3: 800, 4: 975, 5: 1150})
MARVIN_GARDENS = Property('MARVIN_GARDENS', 1, yellow, [280, 150], {0: 24, 1: 120, 2: 360, 3: 850, 4: 1025, 5: 1200})
PACIFIC_AVENUE = Property('PACIFIC_AVENUE', 1, green, [300, 200], {0: 26, 1: 130, 2: 390, 3: 900, 4: 1100, 5: 1275})
NORTH_CAROLINA_AVENUE = Property('NORTH_CAROLINA_AVENUE', 1, green, [300, 200], {0: 26, 1: 130, 2: 390, 3: 900, 4: 1100, 5: 1275})
PENNSYLVANIA_AVENUE = Property('PENNSYLVANIA_AVENUE', 1, green, [320, 200], {0: 28, 1: 150, 2: 450, 3: 1000, 4: 1200, 5: 1400})
PARK_PLACE = Property('PARK_PLACE', 1, darkblue, [350, 200], {0: 35, 1: 175, 2: 500, 3: 1100, 4: 1300, 5: 1500})
BOARDWALK = Property('BOARDWALK', 1, darkblue, [400, 200], {0: 50, 1: 200, 2: 600, 3: 1400, 4: 1700, 5: 2000})

Lcases = []

p = Player('player')