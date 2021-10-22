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
        self.diviner_list = []
        self.player_map = {}
        self.tabletop_channel = None

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

    @commands.command()
    async def register(self, ctx, *args):
        num_arg_error = False

        if (len(args) > 0):
            if (args[0] == "tabletop"):
                if(ctx.author.guild_permissions.administrator):
                    if(len(args) == 2):
                        channel = None
                        channel_id = args[1].replace('<#','').replace('>','')

                        if (channel_id.isnumeric()):
                            channel = ctx.bot.get_channel(int(channel_id))

                        if (channel != None):
                            self.tabletop_channel = channel
                            await ctx.channel.send("Tabletop channel successfully set.")
                        else:
                            await ctx.channel.send("ERROR: Invalid channel.")

                    else:
                        num_arg_error = True
                else:
                    await ctx.channel.send("ERROR: You do not have permission to use this command.")
            
            elif (args[0] == "player"):
                player_id = ctx.author.id

                if player_id not in self.player_map:
                    self.player_map[player_id] = len(self.player_map)
                    self.diviner_list.append(Diviner())
                    self.deck_list.append(Deck())
                    await ctx.channel.send(f"Registered player {ctx.author.name}")

                else:
                    await ctx.channel.send(f"Player {ctx.author.name} already registered")

            else:
                await ctx.channel.send("ERROR: Invalid argument")
        else:
            num_arg_error = True

        if (num_arg_error):
            await ctx.channel.send("ERROR: Insufficient number of arguments")

    @commands.command()
    async def play(self, ctx, *args):
        if (self.tabletop_channel == None):
            await ctx.channel.send("Tabletop channel not set.")
        else:
            await self.tabletop_channel.send("Test")


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
