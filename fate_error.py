from discord.enums import MessageType
from discord.ext import commands

from fate_io import MessageType
from fate_io import sendMessage

class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            message = "You do not have permission to use this command."
        elif isinstance(error, commands.CommandError):
            message = str(error)

        await sendMessage(message, ctx.channel, MessageType.ERROR)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(ErrorHandler(bot))