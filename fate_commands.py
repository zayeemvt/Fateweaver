import discord
from discord import colour
from discord.ext import commands


import fate_io
from tarot_deck import Card
from tarot_deck import Deck
from tarot_deck import Diviner
from fate_io import CardActionType, MessageType, sendCardInfo
from fate_io import sendMessage

class Player(Diviner):
    def __init__(self, player: discord.Member) -> None:
        super().__init__()
        self.member_data = player
        self.deck = Deck()

    def draw(self):
        return super().draw(self.deck)

    def shuffleDeck(self):
        super().shuffleDeck(self.deck)


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
            raise commands.UserInputError("Invalid aspect argument.")

    @commands.command(name="register")
    async def registerPlayer(self, ctx: commands.Context) -> None:
        registered_players = [player.member_data for player in self.player_list]

        if ctx.author not in registered_players:
            new_player = Player(ctx.author)
            new_player.shuffleDeck()
            self.player_list.append(new_player)
            await sendMessage(f"Registered player {ctx.author}", ctx.channel, MessageType.SUCCESS)

        else:
            raise commands.CommandError(f"Player {ctx.author} already registered")

    @commands.command(name="draw")
    async def drawCard(self, ctx: commands.Context) -> None:
        player = next((player for player in self.player_list if player.member_data == ctx.author), None)
        if (player != None):
            card = player.draw()

            if card is not None:
                await sendCardInfo(ctx.author.nick, card, ctx.channel, CardActionType.DRAW)
            else:
                raise commands.CommandError("Cannot draw card from empty deck.")
        else:
            raise commands.CommandError("You are not a registered player.")

    @commands.command(name="play")
    async def playCard(self, ctx: commands.Context, *args) -> None:
        if (self.tabletop_channel == None):
            raise commands.CommandError("Tabletop channel not set.")
        else:
            await sendMessage("Test", self.tabletop_channel)

# For loading Cog
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Fateweaver(bot))