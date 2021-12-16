from random import shuffle
import json

class Card:
    """
    A class used to represent a single card
    """

    def __init__(self, id: int, number: str, name: str, keys: list, desc: str, img_link: str) -> None:
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
    """
    A class used to represent a deck of cards
    """

    def __init__(self) -> None:
        self.cards = []

        # Load cards from JSON
        with open("cards.json") as file:
            card_dict: dict = json.load(file)

        # Instantiate data as Card objects
        for card in card_dict["cards"]:
            card = Card(card["id"], card["number"], card["name"], card["keywords"], card["description"], card["image"])
            self.cards.append(card)

    def shuffle(self) -> None:
        """Shuffle the deck of cards"""

        shuffle(self.cards)

    def drawCard(self):
        """Draw a card from the top of the deck"""

        if len(self.cards) == 0:
            # Return nothing if empty deck
            return None
        else:
            # Pop the topmost card
            return self.cards.pop(0)

    def insertCard(self, card: Card):
        """Add a card to the bottom of the deck"""

        self.cards.append(card)

    def __str__(self) -> str:
        return '\n'.join(str(card) for card in self.cards)

class Diviner:
    """
    A class used to represent the person drawing and using cards
    """
    
    def __init__(self):
        self.hand = []
        self.discard = []

    def draw(self, deck: Deck) -> Card:
        """Draw a card from the top of the deck"""

        card = deck.drawCard()

        # Check in case of empty deck
        if card is not None:
            card.show()
            self.hand.append(card)

        # Return the card for output information purposes
        return card

    def showHand(self):
        """Display the current cards drawn"""

        for card in self.hand:
            card.show()

    def sortHand(self):
        """Sort cards in hand and in discard pile
        
        This function may get deprecated to work with other, future functions."""

        # Sort by card ID
        self.hand.sort(key=lambda card: card.id)
        self.discard.sort(key=lambda card: card.id)

    def playCard(self, card_name: str):
        """Use the specified card, if it is in your hand"""

        # card_name = card_name.lower()

        # Search for the card
        card = next((card for card in self.hand if card.name == card_name), None)

        # If successful, remove it from hand and place in discard pile
        if (card != None):
            card.show()
            self.hand.remove(card)
            self.discard.append(card)

    def shuffleDeck(self, deck: Deck):
        """Return all cards in hand and discard to the deck, then shuffle"""

        # Get list of all cards on player
        player_cards = self.hand + self.discard

        # Put every card back into the deck
        for card in player_cards:
            deck.insertCard(card)

        # Empty out hand and discard pile
        self.hand.clear()
        self.discard.clear()

        # Shuffle the deck with all of the cards
        deck.shuffle()