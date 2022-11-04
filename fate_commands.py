import discord
from discord.ext import commands

from tarot_deck import Card, Deck, Diviner, generateCardList, getCard, findCardIndex
from fate_io import CardActionType, MessageType, sendHandInfo, sendMessage, sendCardInfo, sendDeckInfo

MAX_DRAW = 5

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

class Guild():
    """
    A class that represents an individual Discord server
    """

    def __init__(self, guild: discord.guild) -> None:
        self.tabletop_channel = None
        self.player_list = [Player(player) for player in guild.members]

    def findPlayer(self, user: discord.Member) -> Player:
        # Search for player in list
        player = next((player for player in self.player_list if player.id == user.id), None)

        # If player is not in the list, add them
        if player == None:
            self.player_list.append(Player(user))
            player = self.player_list[-1]
        
        return player


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
        guild = self.getGuild(ctx.guild)

        if channel in ctx.guild.channels:
            guild.tabletop_channel = channel
            await sendMessage("Tabletop channel successfully set.", ctx.channel, MessageType.SUCCESS)
        else:
            raise commands.UserInputError(f"Cannot find channel #{' '.join(channel)}")

    @commands.command(name="reset")
    @commands.has_guild_permissions(administrator=True)
    async def resetPlayer(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Resets a player's entire deck/hand"""

        if user != None:
            player = self.getPlayer(ctx.guild, user)
            player.shuffleDeck()
            message = user.display_name + " reset."
        else:
            for player in self.getGuild(ctx.guild).player_list:
                player.shuffleDeck()
            message = "All players reset."

        await sendMessage(message, ctx.channel, MessageType.SUCCESS)

    @commands.command(name="peek")
    @commands.has_guild_permissions(administrator=True)
    async def peekHand(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Shows a player's entire hand and deck"""

        player = self.getPlayer(ctx.guild, user)

        # Print info to terminal
        print(user.display_name + "'s hand:")
        player.showHand()

        # Send message to Discord
        await sendDeckInfo(user.display_name, player.getSortedHand(), player.getDiscard(), player.getDeck(), ctx.channel)

    @commands.command(name="draw")
    async def drawCard(self, ctx: commands.Context, arg:int = None) -> None:
        """Draws a card from the invoker's deck"""

        player = self.getPlayer(ctx.guild, ctx.author)

        if arg is None or arg < 1:
            arg = 1
        elif arg > MAX_DRAW:
            arg = MAX_DRAW

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

        player = self.getPlayer(ctx.guild, ctx.author)

        # Print info to terminal
        print(ctx.author.display_name + "'s hand:")
        player.showHand()

        # Send message to Discord
        await sendHandInfo(ctx.author.display_name, player.getSortedHand(), player.getDiscard(), len(player.deck.card_nums), ctx.channel)
        

    @commands.command(name="play")
    async def playCard(self, ctx: commands.Context, *args) -> None:
        """Plays specified card from invoker's hand, if it exists"""
        guild = self.getGuild(ctx.guild)

        # Check if there is a tabletop channel
        if (guild.tabletop_channel == None):
            raise commands.CommandError("Tabletop channel not set.")
        
        player = self.getPlayer(ctx.guild, ctx.author)

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
            await sendCardInfo(ctx.author.display_name, card, guild.tabletop_channel, CardActionType.PLAY)

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

        player = self.getPlayer(ctx.guild, ctx.author)

        player.shuffleDeck()

        await sendMessage("All of your cards have been reshuffled into the deck.", ctx.channel, MessageType.SUCCESS)

    def getGuild(self, guild: discord.guild) -> Guild:
        # Check if guild exists in database
        if guild.id not in self.guild_data:
            # If not, generate player list
            self.guild_data[guild.id] = Guild(guild)
        
        return self.guild_data[guild.id]

    def getPlayer(self, guild: discord.guild, user: discord.Member) -> Player:
        return self.getGuild(guild).findPlayer(user)



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fateweaver(bot))