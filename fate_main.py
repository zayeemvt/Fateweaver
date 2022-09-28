"""

fate_main.py

The main file for the Fateweaver bot.

"""

import os
import discord
from discord.ext import commands
import asyncio

from dotenv import load_dotenv

from fate_commands import Fateweaver

## Discord bot script
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="~", intents=intents)

async def load_extensions():
    await bot.load_extension("fate_commands")
    await bot.load_extension("fate_error")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())
















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
