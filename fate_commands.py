import discord
from discord.ext import commands

from tarot_deck import Card, Deck, Diviner
from fate_io import CardActionType, MessageType, sendHandInfo, sendMessage, sendCardInfo

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

        self.checkPlayerRegistered(player)

        print(player.member_data.nick + " drew a card")
        card = player.draw()

        if card is not None:
            player.sortHand()
            await sendCardInfo(player.member_data.nick, card, ctx.channel, CardActionType.DRAW)
        else:
            raise commands.CommandError("Cannot draw card from empty deck.")

    @commands.command(name="hand")
    async def showHand(self, ctx: commands.Context) -> None:
        player = next((player for player in self.player_list if player.member_data == ctx.author), None)

        self.checkPlayerRegistered(player)

        print(player.member_data.nick + "'s hand:")
        player.showHand()

        await sendHandInfo(player.member_data.nick, player.hand, player.discard, len(player.deck.cards), ctx.channel)
        

    @commands.command(name="play")
    async def playCard(self, ctx: commands.Context, *args) -> None:
        if (self.tabletop_channel == None):
            raise commands.CommandError("Tabletop channel not set.")
        
        player = next((player for player in self.player_list if player.member_data == ctx.author), None)

        self.checkPlayerRegistered(player)

        card = next((card for card in player.hand if any(key.lower() in card.keywords for key in args)), None)

        if (card == None):
            raise commands.CommandError(f"Could not find card with keyword(s) \"{' '.join(args)}\" in your hand.")
        else:        
            print(player.member_data.nick + " played a card")
            player.playCard(card.name)
            await sendCardInfo(player.member_data.nick, card, self.tabletop_channel, CardActionType.PLAY)
            await sendMessage(f"You played {card.name}.", ctx.channel, MessageType.SUCCESS)

    @commands.command(name="shuffle")
    async def shuffleCards(self, ctx: commands.Context, *args) -> None:
        player = next((player for player in self.player_list if player.member_data == ctx.author), None)

        self.checkPlayerRegistered(player)

        player.shuffleDeck()

        await sendMessage("All of your cards have been reshuffled into the deck.", ctx.channel, MessageType.SUCCESS)

    def checkPlayerRegistered(self, player) -> None:
        if (player == None):
            raise commands.CommandError("You are not a registered player.")

# For loading Cog
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Fateweaver(bot))