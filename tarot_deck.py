from random import shuffle
import json

class Card:
    def __init__(self, id: int, number: str, name: str, keys: list, desc: str, img_link: str):
        self.id = id
        self.number = number
        self.name = name
        self.keywords = keys
        self.description = desc
        self.image = img_link

    def show(self):
        print(str(self))

    def __str__(self) -> str:
        return self.number + " " + self.name + "\n" + self.description

class Deck:
    def __init__(self) -> None:
        self.cards = []

        with open("cards.json") as file:
            card_dict: dict = json.load(file)

        for card in card_dict["cards"]:
            card = Card(card["id"], card["number"], card["name"], card["keywords"], card["description"], card["image"])
            self.cards.append(card)

    def shuffle(self) -> None:
        shuffle(self.cards)

    def drawCard(self):
        if len(self.cards) == 0:
            return None
        else:
            return self.cards.pop(0)

    def insertCard(self, card):
        self.cards.append(card)

    def __str__(self) -> str:
        return '\n'.join(str(card) for card in self.cards)

class Diviner:
    def __init__(self):
        self.hand = []
        self.discard = []

    def draw(self, deck):
        card = deck.drawCard()

        if card is not None:
            card.show()
            self.hand.append(card)

        return card

    def showHand(self):
        for card in self.hand:
            card.show()

    def sortHand(self):
        self.hand.sort(key=lambda card: card.id)
        self.discard.sort(key=lambda card: card.id)

    def playCard(self, card_name):
        # card_name = card_name.lower()
        card = next((card for card in self.hand if card.name == card_name), None)
        if (card != None):
            card.show()
            self.hand.remove(card)
            self.discard.append(card)

    def shuffleDeck(self, deck):
        player_cards = self.hand + self.discard
        for card in player_cards:
            deck.insertCard(card)
        self.hand.clear()
        self.discard.clear()
        deck.shuffle()