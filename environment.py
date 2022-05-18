# MONOPOLY VERSION USA
from random import randint, choices


# ----- classes -----

class Player:
    def __init__(self, name: str, network):
        self.name = name
        self.network = network
        self.doubleCount = 0
        self.balance = 1500
        self.hand = []
        self.pos = 0
        self.location = Lcases[0]
        self.jailCount = 0
        self.dicesVal = 0

    def roll(self, bot_action, dice1=randint(1, 6), dice2=randint(1, 6)) -> None:
        if self.jailCount == 0:
            self.dicesVal = dice1 + dice2
            self.pos += self.dicesVal
            # replaces go action
            if self.pos >= 40:
                self.balance += 200
                self.pos -= 40
            location: Box = Lcases[self.pos]
            self.location = location
            print(self.pos, location.name)
            if isinstance(location, Property):
                if location.owner is None:
                    # if the property is free to buy
                    if round(bot_action[0], 0):
                        price = location.price[0]
                        if self.balance >= price:
                            location.buy(self)

                else:
                    location.pay(self)
                    if self.balance < 0:
                        self.bankruptcy(location.owner)


            else:
                self.location.action(self)
        else:
            print(f"jailCount : {self.jailCount}")
            self.location.action(self)

        if dice1 == dice2:
            self.doubleCount += 1
            if self.doubleCount == 3:
                self.doubleCount = 0
                go_to_jail(self)
                return
                # !!! jail
            self.roll()
        else:
            self.doubleCount = 0

    def bankruptcy(self, creditor=None) -> None:
        totalValue = self.balance + sum(int(prop.price[0] + prop.houses * prop.price[1] / 2) for prop in self.hand)
        print(f"valeur du patrimoine + balance : {totalValue}")
        if totalValue < 0:
            if creditor is not None:
                creditor.balance += self.balance
            Lplayers.remove(self)
            print("bah t'as perdu mec")
            # !!! défaite

        else:
            while True:
                try:
                    print(f"debt: {-self.balance}")

                    if self.balance >= 0:
                        break

                    ans = int(input(f"Where do you want to sell ? (enter the position)"))
                    property = Lcases[ans]
                    assert isinstance(property, Property) and property.owner == self

                    for prop in property.group:
                        if prop.houses > property.houses:
                            raise ValueError

                    if property.houses == 0:
                        property.owner = None
                        self.hand.remove(property)
                        self.balance += property.price[0]
                        for prop in property.group:
                            prop.update_bonus(prop, self)
                    else:
                        property.houses -= 1
                        self.balance += int(property.price[1] / 2)
                        print(int(property.price[1] / 2))

                except (AssertionError, IndexError, ValueError):
                    print('wrong input')

    def ask_bot(self) -> list:
        observation = [self.balance,
                       0,
                       0,
                       0,
                       0,
                       0,
                       0,
                       0,
                       0,
                       0,
                       0,
                       brown[0],
                       skyblue[0],
                       pink[0],
                       orange[0],
                       red[0],
                       yellow[0],
                       green[0],
                       darkblue[0],
                       companies[0],
                       Lrailroads[0]
                       ]

        if self.location.group:
            observation[self.location.group.id + 1] = 1

        action = self.network.activate(observation)
        return action

    def play(self, dice1=randint(1, 6), dice2=randint(1, 6)) -> None:
        action = self.ask_bot()
        self.roll(dice1, dice2, action)

        # TRADE
        if round(action[1], 0) == 1.0:
            # if the bot wants to trade
            trade_confidences = action[2: 12]
            sorted_trade_requests = sorted([[confidence, group] for confidence, group in zip(trade_confidences, Lgroups)])

            for confidence, group in sorted_trade_requests:
                for prop in group:
                    if prop.owner not in [None, self]:
                        # if prop is in the hand of an adversary
                        price = prop.price[0] * (0.5 + group.bought_ratio)
                        if self.balance >= price:
                            prop.buy(self)
                            break

        # HOUSES
        n_houses = action[12]
        if n_houses:
            # if the network wants to trade

            house_confidences = action[13, 21]

            Lhouses = [0 for _ in range(8)]
            for _ in range(8):
                index = choices(house_confidences, range(8))[0]
                Lhouses[index] += 1

            for i in range(8):
                Lgroups[i].buy_houses(self.Lhouses[i])


class Group:
    def __init__(self, name: str, size: int, id: int):
        self.name = name
        self.size = size
        self.id = id
        self.list = []
        self.bought_ratio = 0

    def buy_houses(self, player, n):
        Lhouses = [prop.houses for prop in self.list]

        # find the index of the min of Lhouses prioritizing a bigger index
        minval = 0
        minindex = 2
        for i in range(self.size):
            if Lhouses[-i - 1] < minval:
                minval = Lhouses[-i - 1]
                minindex = self.size - i - 1

        beginning_prop = self.list[minindex]
        # if the max of houses has not been reached on all properties of self
        while n != 0 and beginning_prop.houses < beginning_prop.max_houses and player.balance >= beginning_prop.price[1]:
            index = (minindex - i) % self.size
            self.list[index].houses += 1
            player.balance -= beginning_prop.price[1]


class Box:
    def __init__(self, name: str, pos: int):
        global Lcases
        self.name = name
        self.pos = pos
        Lcases.append(self)


class Property(Box):
    def __init__(self, name: str, pos: int, group: Group, price: list, rent: dict, update_bonus: callable):
        # pos = int 0<=pos<=40 ; price = [priceCase, priceHouse]
        super().__init__(name, pos)
        self.houses = 0
        self.group = group
        self.price = price
        self.rent = rent
        self.owner = None
        self.group.list.append(self)
        self.bonus = 1
        self.update_bonus = update_bonus
        self.max_houses = len(self.rent) - 1

    def buy(self, player: Player) -> None:
        player.balance -= self.price[0]
        self.owner = player
        player.hand.append(self)
        self.update_bonus(self, player)
        self.group.bought_ratio + 1/self.group.size


    def pay(self, player: Player):
        # player pays to self.owner
        # !!! faillite
        if self.houses == 0:
            if self.pos in [12, 28]:
                # 12 and 28 correspond to the positions of the two companies
                price = self.bonus * player.dicesVal
            else:
                price = self.rent[0] * self.bonus
        else:
            price = self.rent[self.houses]
        player.balance -= price
        self.owner.balance += price
        if player.balance < 0:
            player.bankruptcy(self.owner)


class Special(Box):
    def __init__(self, name: str, pos: int, action: callable):  # pos = int 0<=pos<=40
        super().__init__(name, pos)
        self.action = action
        self.group = None



# ----- functions for updating bonuses -----

def property_bonus(property: Property, player: Player) -> None:
    # if one of the owners of the properties of the group is different it changes bonuses to 1 else changes to 2
    for neighbour in property.group:
        if neighbour.owner != player:
            # changes all bonuses of the group to 1
            for prop in property.group:
                prop.bonus = 1
            return
    # changes all bonuses to 2
    for prop in property.group:
        prop.bonus = 2


def railroad_bonus(property: Property, player: Player) -> None:
    # multiplies the bonus by 2 for every railroad that a player holds
    Lowned = []
    n = 0.5
    for railroad in Lrailroads:
        if railroad.owner == player:
            n *= 2
            Lowned.append(railroad)
    for railroad in Lrailroads:
        railroad.bonus = int(n)


def company_bonus(property: Property, player: Player) -> None:
    # if one of the owners of the properties of the group is different it changes bonuses to 4 else changes to 10
    for neighbour in property.group:
        if neighbour.owner != player:
            # changes all bonuses of the group to 4
            for prop in property.group:
                prop.bonus = 4
            return
    # changes all bonuses to 10
    for prop in property.group:
        prop.bonus = 10


# ----- functions for special boxes -----

def go(player: Player) -> None:
    # already taken into account in player.action()
    pass


def chance(player: Player) -> None:
    i = randint(0, 15)
    card = Lchance[i]
    print(card[0].__name__, card[1])
    f = card[0]
    attribute = card[1]
    f.attribute = attribute
    f(player)
    del Lchance[i]
    Lchance.append(card)


def community_chest(player: Player) -> None:
    i = randint(0, 15)
    card = Lcomchest[i]
    print(card[0].__name__, card[1])
    f = card[0]
    attribute = card[1]
    f.attribute = attribute
    f(player)
    del Lcomchest[i]
    Lcomchest.append(card)


def go_to_jail(player: Player) -> None:
    # go_to_jail is used for property.action but also for chance cards
    player.pos = 10
    player.location = Lcases[10]
    player.jailCount += 1


fees = 0
def tax100(player: Player) -> None:
    global fees
    player.balance -= 100  # !!! faillite
    fees += 100


def tax200(player: Player) -> None:
    global fees
    player.balance -= 200  # !!! faillite
    fees += 200


def free_parking(player: Player) -> None:
    global fees
    player.balance += fees
    fees = 0


def jail(player: Player) -> None:
    if player.jailCount != 0:
        dice1 = randint(1, 6)
        dice2 = randint(1, 6)
        print(f"dice1 : {dice1}, dice 2 : {dice2}")
        if dice1 == dice2:
            print('mec t sorti de prison poissonFdp')
            player.jailCount = 0
            player.roll(dice1, dice2)
        elif player.jailCount == 3:
            player.balance -= 50
            player.jailCount = 0
            print("t'as payé mec parce que tu forces")
            player.roll()
            # !!! faillite
        else:
            player.jailCount += 1


# ----- chance cards + community chest cards -----

def go_to(player: Player) -> None:
    # goTo.attribute is the position of the location
    pos = go_to.attribute
    if player.pos >= pos:
        player.balance += 200
    player.pos = pos
    player.location = Lcases[pos]
    player.location.action(player)


def money_transfer(player: Player) -> None:
    # money.attribute is the amount of money added to player.balance
    player.balance += money_transfer.attribute


def go_to_nearest(player: Player) -> None:
    # go_to_nearest.attribute is either 'r' for railroad or 'c' for company
    typ = go_to_nearest.attribute

    if typ == 'r':
        # test opti à faire
        pos = ((player.pos+5)//10)*10+5

    elif typ == 'c':
        if 12 <= player.pos < 28:
            pos = 28
        else:
            pos = 12

    player.pos = pos
    player.location = Lcases[pos]
    player.location.action(player)


def repairs(player: Player):
    # repairs.attribute is the price player has to pay for each house
    n = 0
    for prop in player.hand:
        n += prop.houses
    player.balance -= n * repairs.attribute
    # !!! faillite


def out_of_jail(player: Player) -> None:
    # no attribute used
    player.jailCount -= 1


Lchance = [(go_to, 0), (go_to, 5), (go_to, 11), (go_to, 24), (go_to, 39), (money_transfer, 150), (money_transfer, -15),
           (money_transfer, -100), (money_transfer, -35), (go_to_nearest, 'c'), (go_to_nearest, 'c'),
           (go_to_nearest, 'r'), (go_to_nearest, 'r'), (repairs, 25), (out_of_jail, None), (go_to_jail, None)]


Lcomchest = [(go_to, 0), (money_transfer, 25), (money_transfer, 100), (money_transfer, 10), (money_transfer, 50),
             (money_transfer, 200), (money_transfer, -50), (money_transfer, 100), (money_transfer, 100),
             (money_transfer, -50), (money_transfer, -100), (money_transfer, 20), (money_transfer, 40),
             (repairs, 40), (out_of_jail, None), (go_to_jail, None)]


# ----- env reset -----

def reset():
    global brown, skyblue, pink, orange, red, yellow, green, darkblue, companies, Lrailroads, GO, MEDITERRANEAN_AVENUE,\
        COMMUNITY_CHEST1, BALTIC_AVENUE, INCOME_TAX, READING_RAILROAD, ORIENTAL_AVENUE, CHANCE1, VERMONT_AVENUE, \
        CONNECTICUT_AVENUE, JAIL, ST_CHARLES_PLACE, ELECTRIC_COMPANY, STATES_AVENUE, VIRGINIA_AVENUE, \
        PENNSYLVANIA_RAILROAD, ST_JAMES_PLACE, COMMUNITY_CHEST2, TENNESSEE_AVENUE, NEW_YORK_AVENUE, FREE_PARKING, \
        KENTUCKY_AVENUE, CHANCE2, INDIANA_AVENUE, ILLINOIS_AVENUE, B_O_RAILROAD, ATLANTIC_AVENUE, VENTNOR_AVENUE, \
        WATER_COMPANY, MARVIN_GARDENS, GO_TO_JAIL, PACIFIC_AVENUE, NORTH_CAROLINA_AVENUE, COMMUNITY_CHEST3, \
        PENNSYLVANIA_AVENUE, SHORT_LINE, CHANCE3, PARK_PLACE, LUXURY_TAX, BOARDWALK, p1, p2, Lplayers, Lcases, Lgroups


    brown = Group('brown', 2, 0)
    skyblue = Group('skyblue', 3, 1)
    pink = Group('pink', 3, 2)
    orange = Group('orange', 3, 3)
    red = Group('red', 3, 4)
    yellow = Group('yellow', 3, 5)
    green = Group('green', 3, 6)
    darkblue = Group('darkblue', 2, 7)
    companies = Group('companies', 2, 8)
    Lrailroads = Group('railroads', 4, 9)


    Lcases = []
    Lgroups = [brown,
               skyblue,
               pink,
               orange,
               red,
               yellow,
               green,
               darkblue,
               companies,
               Lrailroads]

    GO = Special('GO', 0, go)
    MEDITERRANEAN_AVENUE = Property('MEDITERRANEAN_AVENUE', 1, brown, [60, 50], {0: 2, 1: 10, 2: 30, 3: 90, 4: 160, 5: 250}, property_bonus)
    COMMUNITY_CHEST1 = Special('COMMUNITY_CHEST', 2, community_chest)
    BALTIC_AVENUE = Property('BALTIC_AVENUE', 3, brown, [60, 50], {0: 4, 1: 20, 2: 60, 3: 180, 4: 320, 5: 450}, property_bonus)
    INCOME_TAX = Special('INCOME_TAX', 4, tax200)
    READING_RAILROAD = Property('READING_RAILROAD', 5, Lrailroads, [200, None], {0: 25}, railroad_bonus)
    ORIENTAL_AVENUE = Property('ORIENTAL_AVENUE', 6, skyblue, [100, 50], {0: 6, 1: 30, 2: 90, 3: 270, 4: 400, 5: 550}, property_bonus)
    CHANCE1 = Special('CHANCE', 7, chance)
    VERMONT_AVENUE = Property('VERMONT_AVENUE', 8, skyblue, [100, 50], {0: 6, 1: 30, 2: 90, 3: 270, 4: 400, 5: 550}, property_bonus)
    CONNECTICUT_AVENUE = Property('CONNECTICUT_AVENUE', 9, skyblue, [120, 50], {0: 8, 1: 40, 2: 100, 3: 300, 4: 450, 5: 600}, property_bonus)
    JAIL = Special('JAIL', 10, jail)
    ST_CHARLES_PLACE = Property('ST_CHARLES_PLACE', 11, pink, [140, 100], {0: 10, 1: 50, 2: 150, 3: 450, 4: 625, 5: 750}, property_bonus)
    ELECTRIC_COMPANY = Property('ELECTRIC_COMPANY', 12, companies, [150, None], {}, company_bonus)
    STATES_AVENUE = Property('STATES_AVENUE', 13, pink, [140, 100], {0: 10, 1: 50, 2: 150, 3: 450, 4: 625, 5: 750}, property_bonus)
    VIRGINIA_AVENUE = Property('VIRGINIA_AVENUE', 14, pink, [160, 100], {0: 12, 1: 60, 2: 180, 3: 500, 4: 700, 5: 900}, property_bonus)
    PENNSYLVANIA_RAILROAD = Property('PENNSYLVANIA_RAILROAD', 15, Lrailroads, [200, None], {0: 25}, railroad_bonus)
    ST_JAMES_PLACE = Property('ST_JAMES_PLACE', 16, orange, [180, 100], {0: 14, 1: 70, 2: 200, 3: 550, 4: 750, 5: 950}, property_bonus)
    COMMUNITY_CHEST2 = Special('COMMUNITY_CHEST', 17, community_chest)
    TENNESSEE_AVENUE = Property('TENNESSEE_AVENUE', 18, orange, [180, 100],{0: 14, 1: 70, 2: 200, 3: 550, 4: 750, 5: 950}, property_bonus)
    NEW_YORK_AVENUE = Property('NEW_YORK_AVENUE', 19, orange, [200, 100], {0: 16, 1: 80, 2: 220, 3: 600, 4: 800, 5: 1000}, property_bonus)
    FREE_PARKING = Special('FREE_PARKING', 20, free_parking)
    KENTUCKY_AVENUE = Property('KENTUCKY_AVENUE', 21, red, [220, 150], {0: 18, 1: 90, 2: 250, 3: 700, 4: 875, 5: 1050}, property_bonus)
    CHANCE2 = Special('CHANCE', 22, chance)
    INDIANA_AVENUE = Property('INDIANA_AVENUE', 23, red, [220, 150], {0: 18, 1: 90, 2: 250, 3: 700, 4: 875, 5: 1050}, property_bonus)
    ILLINOIS_AVENUE = Property('ILLINOIS_AVENUE', 24, red, [240, 150], {0: 20, 1: 100, 2: 300, 3: 750, 4: 925, 5: 1100}, property_bonus)
    B_O_RAILROAD = Property('B. & O. RAILROAD', 25, Lrailroads, [200, None], {0: 25}, railroad_bonus)
    ATLANTIC_AVENUE = Property('ATLANTIC_AVENUE', 26, yellow, [260, 150], {0: 22, 1: 110, 2: 330, 3: 800, 4: 975, 5: 1150}, property_bonus)
    VENTNOR_AVENUE = Property('VENTNOR_AVENUE', 27, yellow, [260, 150], {0: 22, 1: 110, 2: 330, 3: 800, 4: 975, 5: 1150}, property_bonus)
    WATER_COMPANY = Property('WATER_COMPANY', 28, companies, [150, None], {}, company_bonus)
    MARVIN_GARDENS = Property('MARVIN_GARDENS', 29, yellow, [280, 150], {0: 24, 1: 120, 2: 360, 3: 850, 4: 1025, 5: 1200}, property_bonus)
    GO_TO_JAIL = Special('GO_TO_JAIL', 30, go_to_jail)
    PACIFIC_AVENUE = Property('PACIFIC_AVENUE', 31, green, [300, 200], {0: 26, 1: 130, 2: 390, 3: 900, 4: 1100, 5: 1275}, property_bonus)
    NORTH_CAROLINA_AVENUE = Property('NORTH_CAROLINA_AVENUE', 32, green, [300, 200], {0: 26, 1: 130, 2: 390, 3: 900, 4: 1100, 5: 1275}, property_bonus)
    COMMUNITY_CHEST3 = Special('COMMUNITY_CHEST', 33, community_chest)
    PENNSYLVANIA_AVENUE = Property('PENNSYLVANIA_AVENUE', 34, green, [320, 200], {0: 28, 1: 150, 2: 450, 3: 1000, 4: 1200, 5: 1400}, property_bonus)
    SHORT_LINE = Property('SHORT_LINE', 35, Lrailroads, [200, None], {0: 25}, railroad_bonus)
    CHANCE3 = Special('CHANCE', 36, chance)
    PARK_PLACE = Property('PARK_PLACE', 37, darkblue, [350, 200], {0: 35, 1: 175, 2: 500, 3: 1100, 4: 1300, 5: 1500}, property_bonus)
    LUXURY_TAX = Special('LUXURY_TAX', 38, tax100)
    BOARDWALK = Property('BOARDWALK', 39, darkblue, [400, 200], {0: 50, 1: 200, 2: 600, 3: 1400, 4: 1700, 5: 2000}, property_bonus)

    p1 = Player('p1', None)
    p2 = Player('p2', None)


    Lplayers = [p1, p2]

    return [Lcases, Lplayers]


def play(player1, player2):
    pass


def step():
    # fait une partie avec 2 bots qui se battent pour leur vie sinon ils meurent
    # cé lah lwa duh pluu phaur : lé plhuu phèbl ceu phon aikrazez
    pass


if __name__ == '__main__':
    reset()
