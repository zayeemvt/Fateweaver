from random import shuffle

CARD_LIST = {0 : "The Fool", 1 : "The Magician", 2 : "The High Priestess", 3 : "The Empress",
         4 : "The Emperor", 5 : "The Hierophant", 6 : "The Lovers", 7 : "The Chariot",
         8 : "Justice", 9 : "The Hermit", 10: "Wheel of Fortune", 11: "Strength",
         12: "The Hanged Man", 13: "Death", 14: "Temperance", 15: "The Devil",
         16: "The Tower", 17: "The Star", 18: "The Moon", 19: "The Sun",
         20: "Judgement", 21: "The World"}

CARD_DESC = {
    "The Fool" : "Igor",
    "The Magician" : "Morgana",
    "The High Priestess" : "Makoto Niijima",
    "The Empress" : "Haru Okumura",
    "The Emperor" : "Yusuke Kitagawa",
    "The Hierophant" : "Sojiro Sakura",
    "The Lovers" : "Ann Takamaki",
    "The Chariot" : "Ryuji Sakamoto",
    "Justice" : "Goro Akechi",
    "The Hermit" : "Futaba Sakura",
    "Wheel of Fortune" : "Chihaya Mifune",
    "Strength" : "Caroline and Justine",
    "The Hanged Man" : "Munehisa Iwai",
    "Death" : "Tae Takemi",
    "Temperance" : "Sadayo Kawakami",
    "The Devil" : "Ichiko Ohya",
    "The Tower" : "Shinya Oda",
    "The Star" : "Hifumi Togo",
    "The Moon" : "Yuuki Mishima",
    "The Sun" : "Toranosuke Yoshida",
    "Judgement" : "Sae Niijima",
    "The World" : "Ren Amamiya",
}

class Card:
    def __init__(self, number, name, desc):
        self.number = number
        self.name = name
        self.description = desc
        self.image = None

    def show(self):
        print(str(self))

    def __str__(self) -> str:
        return str(self.number) + " " + self.name + "\n" + self.description

class Deck:
    def __init__(self):
        self.cards = []
        for number, card in CARD_LIST.items():
            self.cards.append(Card(number, card, CARD_DESC[card]))
            # print(self.cards[number].number, self.cards[number].name)

    def shuffle(self):
        shuffle(self.cards)

    def drawCard(self):
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
        card.show()
        self.hand.append(card)

    def showHand(self):
        for card in self.hand:
            card.show()

    def playCard(self, card_name):
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