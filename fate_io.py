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
        action_string = " drew a card!"
    elif (type == CardActionType.PLAY):
        action_string = "played a card!"

    action_string = player_name + action_string
    card_string = card.number + ". " + card.name
    embed = discord.Embed(title=card_string, description=card.description, color=discord.Colour.gold())
    embed.set_image(url=card.image)
    embed.set_footer(text=action_string, icon_url="https://ffxiv.consolegameswiki.com/mediawiki/images/7/7f/Draw.png")

    return embed

async def sendMessage(message: str, channel: discord.TextChannel, type: MessageType = MessageType.DEFAULT) -> None:
    embed = makeEmbed(message, type)
    await channel.send(embed=embed)

async def sendCardInfo(player_name: str, card: Card, channel: discord.TextChannel, type: CardActionType) -> None:
    embed = makeCardEmbed(player_name, card, type)
    await channel.send(embed=embed)