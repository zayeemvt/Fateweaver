import discord
from discord.ext import commands

from tarot_deck import Card, Deck, Diviner, generateCardList, getCard, findCardIndex
from fate_io import CardActionType, MessageType, sendHandInfo, sendMessage, sendCardInfo

class Player(Diviner):
    """
    A class that represents a player on Discord
    """

    def __init__(self, player: discord.Member) -> None:
        super().__init__()
        self.id = player.id
        self.deck = Deck()
        #TODO: Add shuffle command here after testing phase is over

    def draw(self):
        """Draw a card from the player's own deck"""

        return super().draw(self.deck)

    def shuffleDeck(self):
        """Place all cards back into player's deck, then shuffle"""

        super().shuffleDeck(self.deck)

    # def getName(self) -> str:
    #     if self.member_data.nick is not None:
    #         return self.member_data.nick
    #     else:
    #         return self.member_data.name


class Fateweaver(commands.Cog):
    """
    The main bot for the Fateweaver program
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.guild_data = {}

        self.tabletop_channel = None

        generateCardList()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Function called when bot goes online"""

        # Print debug message
        print(f'{self.bot.user.name} connected')

        # Set online status to show help command
        await self.bot.change_presence(activity=discord.Game(name=f"{self.bot.command_prefix}help"))

    @commands.command(name="ping")
    async def ping(self,ctx: commands.Context) -> None:
        """Basic test command for ping"""

        await sendMessage(f"Pong! {round(self.bot.latency * 1000)}ms", ctx.channel)

    @commands.command(name="tabletop")
    @commands.has_guild_permissions(administrator=True)
    async def setChannel(self, ctx: commands.Context, channel: discord.TextChannel) -> None:
        """ADMIN ONLY
        Sets the tabletop channel, where all game actions are displayed"""

        if channel in ctx.guild.channels:
            self.tabletop_channel = channel
            await sendMessage("Tabletop channel successfully set.", ctx.channel, MessageType.SUCCESS)
        else:
            raise commands.UserInputError(f"Cannot find channel #{' '.join(channel)}")

    @commands.command(name="draw")
    async def drawCard(self, ctx: commands.Context, arg:int = None) -> None:
        """Draws a card from the invoker's deck"""

        player = self.getPlayer(ctx)

        if arg is None or arg < 1:
            arg = 1

        for i in range(0,arg):
            print(ctx.author.display_name + " tried to draw a card")
            card = player.draw() # If deck is empty, returns None

            if card is not None:
                await sendCardInfo(ctx.author.display_name, card, ctx.channel, CardActionType.DRAW)
            else:
                raise commands.CommandError("Cannot draw card from empty deck.")

    @commands.command(name="hand")
    async def showHand(self, ctx: commands.Context) -> None:
        """Display the invoker's hand and discard pile"""

        player = self.getPlayer(ctx)

        # Print info to terminal
        print(ctx.author.display_name + "'s hand:")
        player.showHand()

        # Send message to Discord
        await sendHandInfo(ctx.author.display_name, player.getSortedHand(), player.getDiscard(), len(player.deck.card_nums), ctx.channel)
        

    @commands.command(name="play")
    async def playCard(self, ctx: commands.Context, *args) -> None:
        """Plays specified card from invoker's hand, if it exists"""

        # Check if there is a tabletop channel
        if (self.tabletop_channel == None):
            raise commands.CommandError("Tabletop channel not set.")
        
        player = self.getPlayer(ctx)

        card = None
        
        # Find card in player's hand
        for key in args:
            card = player.playCard(key)

            if card is not None:
                break

        if (card == None):
            raise commands.CommandError(f"Could not find card with keyword(s) \"{' '.join(args)}\" in your hand.")
        else:
            print(ctx.author.display_name + " played a card")

            # Send card play announcement to tabletop channel
            await sendCardInfo(ctx.author.display_name, card, self.tabletop_channel, CardActionType.PLAY)

            # Send confirmation to user
            await sendMessage(f"You played {card.name}.", ctx.channel, MessageType.SUCCESS)

    @commands.command(name="view")
    async def viewCard(self, ctx: commands.Context, *args) -> None:
        """Displays the specified card for viewing"""

        index = None
        
        for key in args:
            index = findCardIndex(key)

            if index != -1:
                break
        
        if (index == -1):
            raise commands.CommandError(f"Could not find card with keyword(s) \"{' '.join(args)}\".")
        else:
            card = getCard(index)
            # Send card as message to player
            await sendCardInfo(None, card, ctx.channel, CardActionType.VIEW)


    @commands.command(name="shuffle")
    async def shuffleCards(self, ctx: commands.Context, *args) -> None:
        """Shuffles the invoker's cards back into the deck"""

        player = self.getPlayer(ctx)

        player.shuffleDeck()

        await sendMessage("All of your cards have been reshuffled into the deck.", ctx.channel, MessageType.SUCCESS)

    def getPlayer(self, ctx: commands.Context) -> Player:
        # Check if guild exists in database
        if ctx.guild.id not in self.guild_data:
            # If not, generate player list
            player_list = [Player(player) for player in ctx.guild.members]
            self.guild_data[ctx.guild.id] = player_list

        player_list = self.guild_data[ctx.guild.id]

        # Search for player in list
        player = next((player for player in player_list if player.id == ctx.author.id), None)

        # If player is not in the list, add them
        if player == None:
            self.guild_data[ctx.guild.id].append(Player(ctx.author))
            player = self.guild_data[ctx.guild.id][-1]
        
        return player



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fateweaver(bot))