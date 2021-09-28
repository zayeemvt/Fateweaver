"""

fate_main.py

The main file for the Fateweaver bot.

"""

from tarot_deck import Deck
from tarot_deck import Diviner

if __name__ == '__main__':
    deck = Deck()
    print("\nBase:")
    print(deck)
    print("\nShuffled:")
    # deck.shuffle()
    # print(deck)

    player = Diviner()
    player.shuffleDeck(deck)
    print(deck)

    print("\nPlayer Draws...")
    player.draw(deck)
    player.draw(deck)
    player.draw(deck)

    print("\nPlayer Hand:")
    player.showHand()

    print("\nPlayer Plays...")
    player.playCard(player.hand[0].name)
    player.playCard(player.hand[0].name)
    
    print("\nCurrent Deck:")
    print(deck)
    print(len(deck.cards))

    player.shuffleDeck(deck)
    print("\nDeck After Player Shuffle:")
    print(deck)
    print(len(deck.cards))

