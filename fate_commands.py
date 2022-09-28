import discord
from discord.ext import commands

from tarot_deck import Card, Deck, Diviner, generateCardList
from fate_io import CardActionType, MessageType, sendHandInfo, sendMessage, sendCardInfo

class Player(Diviner):
    """
    A class that represents a player on Discord
    """

    def __init__(self, player: discord.Member) -> None:
        super().__init__()
        self.member_data = player
        self.deck = Deck()

    def draw(self):
        """Draw a card from the player's own deck"""

        return super().draw(self.deck)

    def shuffleDeck(self):
        """Place all cards back into player's deck, then shuffle"""

        super().shuffleDeck(self.deck)

    def getName(self) -> str:
        if self.member_data.nick is not None:
            return self.member_data.nick
        else:
            return self.member_data.name


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

    @commands.command(name="set")
    @commands.has_guild_permissions(administrator=True)
    async def setChannel(self, ctx: commands.Context, aspect: str, channel: discord.TextChannel) -> None:
        """ADMIN ONLY
        Sets the tabletop channel, where all game actions are displayed"""

        if(aspect == "tabletop"): # May deprecate
            self.tabletop_channel = channel
            await sendMessage("Tabletop channel successfully set.", ctx.channel, MessageType.SUCCESS)
        else:
            raise commands.UserInputError("Invalid aspect argument.")

    @commands.command(name="draw")
    async def drawCard(self, ctx: commands.Context) -> None:
        """Draws a card from the invoker's deck"""

        # Check if player is registered
        player = self.getPlayer(ctx)

        print(player.getName() + " drew a card")
        card = player.draw()

        if card is not None:
            # player.sortHand() # Unnecessary, only sort when displaying
            await sendCardInfo(player.getName(), card, ctx.channel, CardActionType.DRAW)
        else:
            raise commands.CommandError("Cannot draw card from empty deck.")

    @commands.command(name="hand")
    async def showHand(self, ctx: commands.Context) -> None:
        """Display the invoker's hand and discard pile"""

        # Check if player is registered
        player = self.getPlayer(ctx)

        # NOTE: Will fail if player does not have a nickname
        print(player.getName() + "'s hand:")
        player.showHand()

        await sendHandInfo(player.getName(), player.getSortedHand(), player.getDiscard(), len(player.deck.card_nums), ctx.channel)
        

    @commands.command(name="play")
    async def playCard(self, ctx: commands.Context, *args) -> None:
        """Plays specified card from invoker's hand, if it exists"""

        # Check if there is a tabletop channel
        if (self.tabletop_channel == None):
            raise commands.CommandError("Tabletop channel not set.")
        
        # Check if player is registered
        player = self.getPlayer(ctx)

        # Find card in player's hand
        # card = next((card for card in player.hand if any(key.lower() in card.keywords for key in args)), None)

        for key in args:
            card = player.playCard(key)

            if card is not None:
                break

        if (card == None):
            raise commands.CommandError(f"Could not find card with keyword(s) \"{' '.join(args)}\" in your hand.")
        else:
            print(player.getName() + " played a card")
            # player.playCard(card.name)

            # Send card play announcement to tabletop channel
            await sendCardInfo(player.getName(), card, self.tabletop_channel, CardActionType.PLAY)

            # Send confirmation to user
            await sendMessage(f"You played {card.name}.", ctx.channel, MessageType.SUCCESS)

    @commands.command(name="shuffle")
    async def shuffleCards(self, ctx: commands.Context, *args) -> None:
        """Shuffles the invoker's cards back into the deck"""

        # Check if player is registered
        player = self.getPlayer(ctx)

        player.shuffleDeck()

        await sendMessage("All of your cards have been reshuffled into the deck.", ctx.channel, MessageType.SUCCESS)

    def getPlayer(self, ctx: commands.Context) -> Player:
        if ctx.guild.id not in self.guild_data:
            player_list = [Player(player) for player in ctx.guild.members]
            self.guild_data[ctx.guild.id] = player_list

        player_list = self.guild_data[ctx.guild.id]

        player = next((player for player in player_list if player.member_data == ctx.author), None)

        if player == None:
            self.guild_data[ctx.guild.id].append(Player(ctx.author))
            player = self.guild_data[ctx.guild.id][-1]
        
        return player



    # def registerPlayer(self, player) -> None:
    #     """Registers a player"""

    #     registered_players = [player.member_data for player in self.player_list] # May deprecate to server data

    #     # Check if user is already registered in server
    #     if player not in registered_players:
    #         # Add user as new player
    #         new_player = Player(player)
    #         new_player.shuffleDeck()
    #         self.player_list.append(new_player)

    #         # await sendMessage(f"Registered player {ctx.author}", ctx.channel, MessageType.SUCCESS)

    # def checkPlayerRegistered(self, player) -> None:
    #     """Verifies if player is registered or not"""

    #     if (player == None):
    #         # raise commands.CommandError("You are not a registered player.")



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fateweaver(bot))