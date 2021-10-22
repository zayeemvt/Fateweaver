import discord
from discord.ext import commands

from tarot_deck import Deck
from tarot_deck import Diviner

class Player(Diviner):
    def __init__(self, player: discord.Member):
        self.id = player
        self.deck = Deck()


class Fateweaver(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.player_list = []
        self.tabletop_channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} connected')
        await self.bot.change_presence(activity=discord.Game(name=f"{self.bot.command_prefix}help"))

    @commands.command(name="ping")
    async def ping(self,ctx: commands.Context):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def echo(self, ctx: commands.Context, *args):
        response = ""
        
        for arg in args:
            response = response + " " + arg

        await ctx.send(response)

    @commands.command(name="set")
    @commands.has_guild_permissions(administrator=True)
    async def setChannel(self, ctx: commands.Context, destination: str, channel: discord.TextChannel):
        if(destination == "tabletop"):
            self.tabletop_channel = channel
            await ctx.send("Tabletop channel successfully set.")

    @setChannel.error
    async def set_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            message = "You do not have permission to use this command."
        else:
            message = str(error)

        await ctx.send("**ERROR**: " + message)


    @commands.command(name="register")
    async def registerPlayer(self, ctx: commands.Context):
        registered_players = [player.id for player in self.player_list]

        if ctx.author not in registered_players:
            new_player = Player(ctx.author)
            self.player_list.append(new_player)
            await ctx.send(f"Registered player {ctx.author}")

        else:
            await ctx.send(f"**ERROR**: Player {ctx.author} already registered")

    @commands.command()
    async def play(self, ctx: commands.Context, *args):
        if (self.tabletop_channel == None):
            await ctx.send("**ERROR**: Tabletop channel not set.")
        else:
            await self.tabletop_channel.send("Test")

# For loading Cog
def setup(bot: commands.Bot):
    bot.add_cog(Fateweaver(bot))