from random import shuffle
import json

card_list = []

def generateCardList():
    """
    Initializes the card list singleton.
    
    YOU MUST CALL THIS FUNCTION FIRST IN ORDER FOR THE REST OF THE MODULE TO WORK!!
    """
    # Load cards from JSON
    with open("cards.json") as file:
        card_dict: dict = json.load(file)

    # Instantiate data as Card objects
    for card in card_dict["cards"]:
        card = Card(card["id"], card["number"], card["name"], card["keywords"],
                    card["short"], card["description"], card["image"])
        card_list.append(card)

def getCard(index: int) -> 'Card':
    """Retrieves Card object from card list"""

    return card_list[index]

def getCardString(index: int) -> str:
    """Retrieves Card object from card list in string format"""

    return str(card_list[index])

def getCardName(index: int) -> str:
    """Retrieves the name of Card object from card list"""

    return card_list[index].name

def getCardKeywords(index: int) -> list[str]:
    """Retrieves the keywords of Card object from card list"""

    return card_list[index].keywords

def printCard(index: int) -> None:
    """Prints Card object from card list to terminal"""

    card_list[index].show()

class Card:
    """
    A class used to represent a single card
    """

    def __init__(self, id: int, number: str, name: str, keys: list, short: str, desc: str, img_link: str) -> None:
        self.id = id
        self.number = number
        self.name = name
        self.keywords = keys
        self.short = short
        self.description = desc
        self.image = img_link

    def show(self):
        print(str(self))

    def __str__(self) -> str:
        return self.number + " " + self.name + "\n" + self.description

class Deck:
    """
    A class used to represent a deck of cards by using an array of card indices
    """

    def __init__(self) -> None:
        self.card_nums = list(range(0, len(card_list)))

    def shuffle(self) -> None:
        """Shuffle the deck of cards"""

        shuffle(self.card_nums)

    def drawCard(self) -> int:
        """Draw a card from the top of the deck"""

        if len(self.card_nums) == 0:
            # Return nothing if empty deck
            return None
        else:
            # Pop the topmost card
            return self.card_nums.pop(0)

    def insertCard(self, card_index: int) -> None:
        """Add a card to the bottom of the deck"""

        self.card_nums.append(card_index)

    def __str__(self) -> str:
        return '\n'.join(getCardString(card_index) for card_index in self.card_nums)


class Diviner:
    """
    A class used to represent the person drawing and using cards
    """

    def __init__(self):
        self.hand = []
        self.discard = []

    def draw(self, deck: Deck) -> Card:
        """Draw a card from the top of the deck"""

        card = None

        card_index = deck.drawCard()

        # Check in case of empty deck
        if card_index is not None:
            # print("Drew card:")
            # printCard(card_index)
            self.hand.append(card_index)
            card = getCard(card_index)

        # Return the card for output information purposes
        return card

    def showHand(self):
        """Display the current cards drawn"""

        # print("Current hand:")

        # for card_index in self.hand:
        #     printCard(card_index)
    
    def getHand(self) -> list[Card]:
        """Returns hand as list of Card objects"""

        return [card_list[index] for index in self.hand]

    def getSortedHand(self) -> list[Card]:
        """Returns hand as SORTED list of Card objects"""

        cards = [card_list[index] for index in self.hand]
        cards.sort(key=lambda card: card.id)

        return cards

    def getDiscard(self) -> list[Card]:
        """Returns discard pile as list of Card objects"""

        return [card_list[index] for index in self.discard]
    
    def getSortedDiscard(self) -> list[Card]:
        """Returns discard pile as SORTED list of Card objects"""
        
        cards = [card_list[index] for index in self.discard]
        cards.sort(key=lambda card: card.id)

        return cards

    def playCard(self, card_name: str) -> Card:
        """Use the specified card, if it is in your hand"""

        card_index = self.findCardIndex(card_name)

        # If successful, remove it from hand and place in discard pile
        if (card_index != -1):
            # print("Played card:")
            # printCard(card_index)
            self.hand.remove(card_index)
            self.discard.append(card_index)
            return card_list[card_index]
        else:
            return None
    
    def findCardIndex(self, card_name: str) -> int:
        """Searches for a card by name and returns the index, if it is in your hand"""

        card_name = card_name.lower()

        if len(self.hand) == 0:
            card_index = -1 

        for card_index in self.hand:
            if getCardName(card_index).lower() == card_name or card_name in getCardKeywords(card_index):
                break
            else:
                card_index = -1
        
        return card_index

    def shuffleDeck(self, deck: Deck) -> None:
        """Return all cards in hand and discard to the deck, then shuffle"""

        # Get list of all cards on player
        player_cards = self.hand + self.discard

        # Put every card back into the deck
        for card_index in player_cards:
            deck.insertCard(card_index)

        # Empty out hand and discard pile
        self.hand.clear()
        self.discard.clear()

        # Shuffle the deck with all of the cards
        deck.shuffle()

if __name__ == "__main__":
    generateCardList()

    myDeck = Deck()
    # myDeck.shuffle()

    # print(myDeck)

    # for i in range(0,3):
    #     print(myDeck.drawCard())

    myPlayer = Diviner()
    myPlayer.draw(myDeck)
    myPlayer.draw(myDeck)
    myPlayer.draw(myDeck)

    myPlayer.showHand()

    myPlayer.playCard("magic")
    myPlayer.playCard("The Fool")
    myPlayer.playCard("Priestess")

    myPlayer.draw(myDeck)

    myPlayer.showHand()
    myPlayer.shuffleDeck(myDeck)

    myPlayer.draw(myDeck)
    myPlayer.draw(myDeck)
