import discord

from enum import Enum

from discord.message import Message

class MessageType(Enum):
    DEFAULT = 1
    ERROR = 2
    SUCCESS = 3

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

async def sendMessage(message: str, channel: discord.TextChannel, type: MessageType = MessageType.DEFAULT) -> None:
    embed = makeEmbed(message, type)
    await channel.send(embed=embed)