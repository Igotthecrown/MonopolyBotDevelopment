from collections import deque
class Game:
    def __init__(self):
        self.board = []
        self.chance_card = deque()
        self.community_chest = deque()
        self.players = []
monopolize = {'brown':2,'lightblue':3,"pink":3,"orange":3,"red":3,"yellow":3,"green":3,"blue":2}
class Player:
    def __init__(self, name, money, game):
        self.name = name
        self.money = money
        self.game = game 
        self.lands = []
        self.cards = []
        self.colors = {'brown':0, 'lightblue':0, "pink":0, "orange":0, "red":0, "yellow":0, "green":0, "blue":0}
        self.position = 0
    def buy(self,land):
        if self.money < land.cost:
            print('You cannot buy this.')
        else:
            #subtract money
            self.money -= land.cost
            #change owner
            land.owner = self
            self.lands.append(land)
            #adding colors
            self.colors[land.color] += 1
            if self.colors[land.color] == monopolize[land.color]:
                land.color_monopoly = True
                for i in self.lands:
                    if i.color == land.color:
                        i.color_monopoly = True
    def pay(self,land):
        if land.houses == 0:
            if land.hotels == 0:
                if land.color_monopoly:
                    self.money -= land.rent * 2
                    land.owner.money += land.rent * 2
                else:
                    self.money -= land.rent
                    land.owner.money += land.rent
            else:
                self.money -= land.hotel
                land.owner.money += land.hotel
        else:
            if land.houses == 1:
                self.money -= land.houses1
                land.owner.money += land.houses1
            elif land.houses == 2:
                self.money -= land.houses2
                land.owner.money += land.houses2
            elif land.houses == 3:
                self.money -= land.houses3
                land.owner.money += land.houses3
            else:
                self.money -= land.houses4
                land.owner.money += land.houses4
    def sell(self):
        pass
    def trade(self):
        pass
    #action happens when there is a owner.
    def action(self,land):
        if land.name == 'JAIL':
            pass
        else:
            if land.owner is None:
                if 'Y' == input('wanna buy land?'):
                    self.buy(land)
            else:
                self.pay(land)
            while self.money < 0:
                pass
    def card_drawing(self,cards):
        drawn_card = cards.popleft()
        drawn_card.drew(self)
        cards.append(drawn_card)
class Tile:
    def __init__(self, name):
        self.name = name
    def landing(self,player):
        print(f'{player.name} landed at {self.name}')
class PropertyTile(Tile):
    def __init__(self,name,cost,rent,houses_hotels_rent,house_cost,hotel_cost,color):
        super().__init__(name)
        self.cost = cost
        self.rent = [rent]+houses_hotels_rent
        self.house_cost = house_cost
        self.hotel_cost = hotel_cost
        self.color = color
        self.color_monopoly = False
        self.owner = None
        self.houses = 0
        self.hotels = 0
class Card:
    def __init__(self,description,card_type,card_value):
        self.description = description
        self.card_type = card_type
        self.card_value = card_value
    def drew(self,player):
        print(f'{player.name} : {self.description}')
        if self.card_type == 'dynamic_move':
            pass
        if self.card_type == 'dynamic_money':
            pass
        if self.card_type == 'money':
            player.money += self.card_value
        if self.card_type == 'move':
            player.position = self.card_value
            player.action(player.game.board[player.position])
            #need some other code for special moves:
            pass
        if self.card_type == 'keep':
            player.cards.append(self.card_value)
class ChanceTile(Tile):
    def __init__(self, name="Chance"):
        super().__init__(name)
    def landing(self, player):
        super().landing(player)  # "OOO landed at Chance"
        player.card_drawing(player.game.chance_card)
class CommunityChest(Tile):
    def __init__(self, name="Community Chest"):
        super().__init__(name)
    def landing(self, player):
        super().landing(player)
        player.card_drawing(player.game.chance_card)