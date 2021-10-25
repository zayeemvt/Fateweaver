import discord

from enum import Enum

from discord.message import Message

from tarot_deck import Card

class MessageType(Enum):
    DEFAULT = 1
    ERROR = 2
    SUCCESS = 3

class CardActionType(Enum):
    DRAW = 1
    PLAY = 2

def makeEmbed(message: str, type: MessageType = MessageType.DEFAULT) -> discord.Embed:
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

def makeCardEmbed(player_name: str, card: Card, type: CardActionType) -> discord.Embed:
    if (type == CardActionType.DRAW):
        action_string = player_name + " drew a card!"
        action_image = "https://ffxiv.consolegameswiki.com/mediawiki/images/7/7f/Draw.png"
    elif (type == CardActionType.PLAY):
        action_string = player_name + "played a card!"
        action_image = "https://ffxiv.consolegameswiki.com/mediawiki/images/9/90/Play.png"

    card_string = card.number + ". " + card.name
    embed = discord.Embed(title=card_string, description=card.description, color=discord.Colour.gold())
    embed.set_image(url=card.image)
    embed.set_footer(text=action_string, icon_url=action_image)

    return embed

def makeHandEmbed(player_name: str, hand: list[Card], discard: list[Card]) -> discord.Embed:
    embed = discord.Embed(title="Drawn Cards", color=discord.Colour.blue())

    if len(hand) > 0:
        hand_string = ""
        for card in hand:
            hand_string = hand_string + card.number + ". " + card.name + " (" + card.description + ")\n"
    else:
        hand_string = None
    
    embed.add_field(name="Cards in Hand", value=hand_string, inline=False)

    if len(discard) > 0:
        card = None
        discard_string = ""
        for card in discard:
            discard_string = discard_string + card.number + ". " + card.name + " (" + card.description + ")\n"
    else:
        discard_string = None

    embed.add_field(name="Discarded Cards", value=discard_string, inline=False)

    embed.set_footer(text=f"Viewing {player_name}'s cards", icon_url="https://ffxiv.consolegameswiki.com/mediawiki/images/f/f0/Minor_Arcana.png")

    return embed

async def sendMessage(message: str, channel: discord.TextChannel, type: MessageType = MessageType.DEFAULT) -> None:
    embed = makeEmbed(message, type)
    await channel.send(embed=embed)

async def sendCardInfo(player_name: str, card: Card, channel: discord.TextChannel, type: CardActionType) -> None:
    embed = makeCardEmbed(player_name, card, type)
    await channel.send(embed=embed)

async def sendHandInfo(player_name: str, hand: list[Card], discard: list[Card], channel: discord.TextChannel) -> None:
    embed = makeHandEmbed(player_name, hand, discard)
    await channel.send(embed=embed)