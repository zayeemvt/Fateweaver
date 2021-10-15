"""

fate_main.py

The main file for the Fateweaver bot.

"""

import os
import discord
from discord.ext import commands

from dotenv import load_dotenv

from tarot_deck import Deck
from tarot_deck import Diviner

## Discord bot script
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# client = discord.Client()

# @client.event
# async def on_ready():
#     for guild in client.guilds:
#         if guild.name == GUILD:
#             break

#     print(
#         f'{client.user} is connected to the following guild:\n'
#         f'{guild.name}(id: {guild.id})'
#         )

# client.run(TOKEN)

# bot = commands.Bot(command_prefix="~")

# @bot.event
# async def on_ready():
#     print(f'{bot.user.name} connected')

# @bot.command()
# async def ping(ctx):
#     await ctx.channel.send("pong")

# @bot.command()
# async def echo(ctx, *args):
#     response = ""
    
#     for arg in args:
#         response = response + " " + arg

#     await ctx.channel.send(response)

# bot.run(TOKEN)

bot = commands.Bot(command_prefix="~")

class Fateweaver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deck_list = []
        self.player_list = []

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} connected')

    @commands.command()
    async def ping(self,ctx):
        await ctx.channel.send("pong")

    @commands.command()
    async def echo(self, ctx, *args):
        response = ""
        
        for arg in args:
            response = response + " " + arg

        await ctx.channel.send(response)

bot.add_cog(Fateweaver(bot))
bot.run(TOKEN)


















## Command line functions
def basicTest(deck, player):
    print("\nBase:")
    print(deck)
    print("\nShuffled:")
    # deck.shuffle()
    # print(deck)

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

if __name__ == '__main__':
    deck = Deck()
    player = Diviner()

    basicTest(deck, player)
