import discord
from discord import colour
from discord.ext import commands


import fate_io
from tarot_deck import Deck
from tarot_deck import Diviner
from fate_io import MessageType
from fate_io import sendMessage

class Player(Diviner):
    def __init__(self, player: discord.Member) -> None:
        self.id = player
        self.deck = Deck()


class Fateweaver(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.player_list = []
        self.tabletop_channel = None

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f'{self.bot.user.name} connected')
        await self.bot.change_presence(activity=discord.Game(name=f"{self.bot.command_prefix}help"))

    @commands.command(name="ping")
    async def ping(self,ctx: commands.Context) -> None:
        await sendMessage(f"Pong! {round(self.bot.latency * 1000)}ms", ctx.channel)

    # @commands.command()
    # async def echo(self, ctx: commands.Context, *args) -> None:
    #     response = ""
        
    #     for arg in args:
    #         response = response + " " + arg

    #     await ctx.send(response)

    @commands.command(name="set")
    @commands.has_guild_permissions(administrator=True)
    async def setChannel(self, ctx: commands.Context, aspect: str, channel: discord.TextChannel) -> None:
        if(aspect == "tabletop"):
            self.tabletop_channel = channel
            await sendMessage("Tabletop channel successfully set.", ctx.channel, MessageType.SUCCESS)
        else:
            await sendMessage("Invalid aspect argument.", ctx.channel, MessageType.ERROR)

    @setChannel.error
    async def setCommandError(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingPermissions):
            message = "You do not have permission to use this command."
        else:
            message = str(error)

        await sendMessage(message, ctx.channel, MessageType.ERROR)


    @commands.command(name="register")
    async def registerPlayer(self, ctx: commands.Context) -> None:
        registered_players = [player.id for player in self.player_list]

        if ctx.author not in registered_players:
            new_player = Player(ctx.author)
            self.player_list.append(new_player)
            await sendMessage(f"Registered player {ctx.author}", ctx.channel, MessageType.SUCCESS)

        else:
            await sendMessage(f"Player {ctx.author} already registered", ctx.channel, MessageType.ERROR)

    @commands.command()
    async def play(self, ctx: commands.Context, *args) -> None:
        if (self.tabletop_channel == None):
            await sendMessage("Tabletop channel not set.", ctx.channel, MessageType.ERROR)
        else:
            await sendMessage("Test", self.tabletop_channel)

# For loading Cog
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Fateweaver(bot))