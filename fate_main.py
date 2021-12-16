"""

fate_main.py

The main file for the Fateweaver bot.

"""

import os
from discord.ext import commands

from dotenv import load_dotenv

## Discord bot script
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="~")

bot.load_extension("fate_commands")
bot.load_extension("fate_error")

bot.run(TOKEN)


















## Command line functions
# def basicTest(deck, player):
#     print("\nBase:")
#     print(deck)
#     print("\nShuffled:")
#     # deck.shuffle()
#     # print(deck)

#     player.shuffleDeck(deck)
#     print(deck)

#     print("\nPlayer Draws...")
#     player.draw(deck)
#     player.draw(deck)
#     player.draw(deck)

#     print("\nPlayer Hand:")
#     player.showHand()

#     print("\nPlayer Plays...")
#     player.playCard(player.hand[0].name)
#     player.playCard(player.hand[0].name)
    
#     print("\nCurrent Deck:")
#     print(deck)
#     print(len(deck.cards))

#     player.shuffleDeck(deck)
#     print("\nDeck After Player Shuffle:")
#     print(deck)
#     print(len(deck.cards))

# if __name__ == '__main__':
#     deck = Deck()
#     player = Diviner()

#     basicTest(deck, player)
