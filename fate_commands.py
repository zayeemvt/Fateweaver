import discord
from discord.ext import commands, tasks

from tarot_deck import Card, Deck, Diviner, generateCardList, getCard, findCardIndex
from fate_io import CardActionType, MessageType, sendHandInfo, sendMessage, sendCardInfo, sendDeckInfo
from fate_data import saveData

MAX_DRAW = 5

class Player(Diviner):
    """
    A class that represents a player on Discord
    """

    def __init__(self, hand: list[int] = None, discard: list[int] = None, deck_cards: list[int] = None) -> None:
        super().__init__(hand, discard)
        self.deck = Deck(deck_cards)
        #TODO: Add shuffle command here after testing phase is over

        if deck_cards is None:
            self.shuffleDeck()

    def draw(self):
        """Draw a card from the player's own deck"""

        return super().draw(self.deck)

    def shuffleDeck(self):
        """Place all cards back into player's deck, then shuffle"""

        super().shuffleDeck(self.deck)

class Guild():
    """
    A class that represents an individual Discord server
    """

    def __init__(self, player_dict: dict[Player], tabletop: int = None) -> None:
        self.tabletop_channel = tabletop
        self.player_list = player_dict

    def findPlayer(self, user: discord.Member) -> Player:
        # Search for player in list
        player = self.player_list.get(user.id, None)

        # If player is not in the list, add them
        if player == None:
            self.player_list[user.id] = Player()
            player = self.player_list[user.id]
        
        return player


class Fateweaver(commands.Cog):
    """
    The main bot for the Fateweaver program
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.guild_data = {}

        generateCardList()
        self.save.start()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Function called when bot goes online"""

        # Print debug message
        print(f'{self.bot.user.name} connected')

        # Set online status to show help command
        await self.bot.change_presence(activity=discord.Game(name=f"{self.bot.command_prefix}help"))

    @tasks.loop(seconds=30.0)
    async def save(self):
        print("Saving data...")
        saveData(self.guild_data)
        print("Data saved.")

    @save.before_loop
    async def before_save(self):
        print("Waiting...")
        await self.bot.wait_until_ready()

    @commands.command(name="ping")
    async def ping(self,ctx: commands.Context) -> None:
        """Basic test command for ping."""

        await sendMessage(f"Pong! {round(self.bot.latency * 1000)}ms", ctx.channel)

    @commands.command(name="tabletop")
    @commands.has_guild_permissions(administrator=True)
    async def setChannel(self, ctx: commands.Context, channel: discord.TextChannel) -> None:
        """(ADMIN ONLY) Sets the server's tabletop channel, where all game actions are displayed."""
        guild = self.getGuild(ctx.guild)

        if channel in ctx.guild.channels:
            guild.tabletop_channel = channel.id
            await sendMessage("Tabletop channel successfully set.", ctx.channel, MessageType.SUCCESS)
        else:
            raise commands.UserInputError(f"Cannot find channel #{' '.join(channel)}")

    @commands.command(name="reset")
    @commands.has_guild_permissions(administrator=True)
    async def resetPlayer(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """(ADMIN ONLY) Resets a player's entire deck/hand (or all players if none are specified)."""

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
    async def peekHand(self, ctx: commands.Context, user: discord.Member) -> None:
        """(ADMIN ONLY) Shows a player's entire hand and deck."""
        if user == None:
            raise commands.UserInputError("Player not specified.")

        player = self.getPlayer(ctx.guild, user)

        # Print info to terminal
        # print(user.display_name + "'s hand:")
        # player.showHand()

        # Send message to Discord
        await sendDeckInfo(user.display_name, player.getSortedHand(), player.getDiscard(), player.getDeck(), ctx.channel)

    @commands.command(name="draw")
    async def drawCard(self, ctx: commands.Context, arg:int = None) -> None:
        """Draw a card from your deck. Specify a number to draw multiple cards at once."""

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
        """Display the your hand, discard pile, and number of cards remaining in your deck."""

        player = self.getPlayer(ctx.guild, ctx.author)

        # Print info to terminal
        print(ctx.author.display_name + "'s hand:")
        player.showHand()

        # Send message to Discord
        await sendHandInfo(ctx.author.display_name, player.getSortedHand(), player.getDiscard(), player.getSortedDeck(), ctx.channel)
        

    @commands.command(name="play")
    async def playCard(self, ctx: commands.Context, *args) -> None:
        """Play a card from your hand."""
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
            await sendCardInfo(ctx.author.display_name, card, self.getTabletop(ctx.guild, guild.tabletop_channel), CardActionType.PLAY)

            # Send confirmation to user
            await sendMessage(f"You played {card.name}.", ctx.channel, MessageType.SUCCESS)

    @commands.command(name="view")
    async def viewCard(self, ctx: commands.Context, *args) -> None:
        """Display any card and its details. The card does not need to be in your hand."""

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
        """Reshuffles all cards in your hand and discard pile back into your deck."""

        player = self.getPlayer(ctx.guild, ctx.author)

        player.shuffleDeck()

        await sendMessage("All of your cards have been reshuffled into the deck.", ctx.channel, MessageType.SUCCESS)

    def getGuild(self, guild: discord.guild) -> Guild:
        # Check if guild exists in database
        if guild.id not in self.guild_data:
            # If not, generate player list
            player_list = {}

            for player in guild.members:
                player_list[player.id] = Player()

            self.guild_data[guild.id] = Guild(player_list)
        
        return self.guild_data[guild.id]

    def getTabletop(self, guild: discord.guild, id: int) -> discord.TextChannel:
        return next((channel for channel in guild.channels if channel.id == id), None)

    def getPlayer(self, guild: discord.guild, user: discord.Member) -> Player:
        return self.getGuild(guild).findPlayer(user)



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fateweaver(bot))