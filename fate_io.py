import discord

from enum import Enum

from discord.message import Message

from tarot_deck import Card

# Classifies messages into different types
class MessageType(Enum):
    DEFAULT = 1
    ERROR = 2
    SUCCESS = 3

# Classifies player actions
class CardActionType(Enum):
    DRAW = 1
    PLAY = 2
    VIEW = 3
    REDRAW = 4

def makeEmbed(message: str, type: MessageType = MessageType.DEFAULT) -> discord.Embed:
    """Used to make general-purpose embeds"""

    embed = discord.Embed(description=message)

    if (type == MessageType.DEFAULT):
        embed.color = discord.Colour.blue()

    elif (type == MessageType.ERROR):
        embed.title = "**Error**"
        embed.color = discord.Colour.red()

    elif (type == MessageType.SUCCESS):
        embed.title = "**Success**"
        embed.color = discord.Colour.green()

    return embed

def makeCardEmbed(player_name: str, avatar_url: str, card: Card, type: CardActionType) -> discord.Embed:
    """Used to make embeds specific to card actions"""
   # Create the embed
    card_string = card.number + ". " + card.name
    embed = discord.Embed(title=card_string, description=card.description, color=discord.Colour.gold())

    # Choose message text and icon
    if (type == CardActionType.DRAW):
        action_string = player_name + " drew a card!"
        action_image = "https://ffxiv.consolegameswiki.com/mediawiki/images/7/7f/Draw.png"
        action_text = "Draw"
    elif (type == CardActionType.PLAY):
        action_string = player_name + " played a card!"
        action_image = "https://ffxiv.consolegameswiki.com/mediawiki/images/9/90/Play.png"
        action_text = "Play"
    elif (type == CardActionType.VIEW):
        action_string = "Viewing card: " + card.name
        action_image = "https://ffxiv.consolegameswiki.com/mediawiki/images/f/f0/Minor_Arcana.png"
        action_text = "View"
    elif (type == CardActionType.REDRAW):
        action_string = player_name + " redrew a card!"
        action_image = "https://ffxiv.consolegameswiki.com/mediawiki/images/6/66/Redraw.png"
        action_text = "Redraw"

    embed.set_image(url=card.image)
    embed.set_author(name=action_text, icon_url=action_image)
    embed.set_footer(text=action_string, icon_url=avatar_url)

    return embed

def makeHandEmbed(player_name: str, avatar_url: str, hand: list[Card], discard: list[Card], deck: list[Card]) -> discord.Embed:
    """Used to make the embed representing the player's hand"""

    embed = discord.Embed(title="Drawn Cards", color=discord.Colour.blue())

    # Add all cards in hand to a string, if there are any
    if len(hand) > 0:
        hand_string = ""
        for card in hand:
            hand_string = hand_string + card.number + ". " + card.name + "\n"
    else:
        hand_string = None
    
    embed.add_field(name="Cards in Hand", value=hand_string, inline=False)

    # Add all cards in discard to a string, if there are any
    if len(discard) > 0:
        card = None
        discard_string = ""
        for card in discard:
            discard_string = discard_string + card.number + ". " + card.name + "\n"
    else:
        discard_string = None

    embed.add_field(name="Discarded Cards", value=discard_string, inline=False)

    if len(deck) > 0:
        card = None
        deck_string = ""
        for card in deck:
            deck_string = deck_string + card.number + ". " + card.name + "\n"
    else:
        deck_string = None

    embed.add_field(name="Remaining Cards in Deck", value=deck_string, inline=False)

    embed.set_author(name="View", icon_url="https://ffxiv.consolegameswiki.com/mediawiki/images/f/f0/Minor_Arcana.png")
    embed.set_footer(text=f"Viewing {player_name}'s cards", icon_url=avatar_url)

    return embed

def makeDeckEmbed(player_name: str, avatar_url: str, hand: list[Card], discard: list[Card], deck: list[Card]) -> discord.Embed:
    """Used to make the embed representing the player's hand"""

    embed = discord.Embed(title="Player Cards", color=discord.Colour.blue())

    # Add all cards in hand to a string, if there are any
    if len(hand) > 0:
        hand_string = ""
        for card in hand:
            hand_string = hand_string + card.number + ". " + card.name + "\n"
    else:
        hand_string = None
    
    embed.add_field(name="Cards in Hand", value=hand_string, inline=False)

    if len(deck) > 0:
        card = None
        deck_string = ""
        for card in deck:
            deck_string = deck_string + card.number + ". " + card.name + "\n"
    else:
        deck_string = None

    embed.add_field(name="Remaining Cards in Deck", value=deck_string, inline=False)

    # Add all cards in discard to a string, if there are any
    if len(discard) > 0:
        card = None
        discard_string = ""
        for card in discard:
            discard_string = discard_string + card.number + ". " + card.name + "\n"
    else:
        discard_string = None

    embed.add_field(name="Discarded Cards", value=discard_string, inline=False)

    embed.set_author(name="View", icon_url="https://ffxiv.consolegameswiki.com/mediawiki/images/f/f0/Minor_Arcana.png")
    embed.set_footer(text=f"Viewing {player_name}'s cards", icon_url=avatar_url)

    return embed

async def sendMessage(message: str, channel: discord.TextChannel, type: MessageType = MessageType.DEFAULT) -> None:
    """API function for sending a message through the bot"""

    embed = makeEmbed(message, type)
    await channel.send(embed=embed)

async def sendCardInfo(player_name: str, avatar_url: str, card: Card, channel: discord.TextChannel, type: CardActionType) -> None:
    """API function for sending card information through the bot"""

    embed = makeCardEmbed(player_name, avatar_url, card, type)
    await channel.send(embed=embed)

async def sendHandInfo(player_name: str, avatar_url: str, hand: list[Card], discard: list[Card], deck: list[Card], channel: discord.TextChannel) -> None:
    """API function for sending hand information through the bot"""
    
    embed = makeHandEmbed(player_name, avatar_url, hand, discard, deck)
    await channel.send(embed=embed)

async def sendDeckInfo(player_name: str, avatar_url: str, hand: list[Card], discard: list[Card], deck: list[Card], channel: discord.TextChannel) -> None:
    """API function for sending hand information through the bot"""
    
    embed = makeDeckEmbed(player_name, avatar_url, hand, discard, deck)
    await channel.send(embed=embed)