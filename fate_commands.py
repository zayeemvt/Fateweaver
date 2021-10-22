from discord.ext import commands

from tarot_deck import Deck
from tarot_deck import Diviner

def setup(bot: commands.Bot):
    bot.add_cog(Fateweaver(bot))

class Fateweaver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deck_list = []
        self.diviner_list = []
        self.player_map = {}
        self.tabletop_channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} connected')

    @commands.command()
    async def ping(self,ctx):
        await ctx.channel.send("pong")

    @commands.command()
    async def echo(self, ctx, *args):
        response = ""
        
        for arg in args:
            response = response + " " + arg

        await ctx.channel.send(response)

    @commands.command()
    async def register(self, ctx, *args):
        num_arg_error = False

        if (len(args) > 0):
            if (args[0] == "tabletop"):
                if(ctx.author.guild_permissions.administrator):
                    if(len(args) == 2):
                        channel = None
                        channel_id = args[1].replace('<#','').replace('>','')

                        if (channel_id.isnumeric()):
                            channel = ctx.bot.get_channel(int(channel_id))

                        if (channel != None):
                            self.tabletop_channel = channel
                            await ctx.send("Tabletop channel successfully set.")
                        else:
                            await ctx.send("**ERROR**: Invalid channel.")

                    else:
                        num_arg_error = True
                else:
                    await ctx.send("**ERROR**: You do not have permission to use this command.")
            
            elif (args[0] == "player"):
                player_id = ctx.author.id

                if player_id not in self.player_map:
                    self.player_map[player_id] = len(self.player_map)
                    self.diviner_list.append(Diviner())
                    self.deck_list.append(Deck())
                    await ctx.send(f"Registered player {ctx.author.name}")

                else:
                    await ctx.send(f"**ERROR**: Player {ctx.author.name} already registered")

            else:
                await ctx.send("**ERROR**: Invalid argument")
        else:
            num_arg_error = True

        if (num_arg_error):
            await ctx.send("**ERROR**: Insufficient number of arguments")

    @commands.command()
    async def play(self, ctx, *args):
        if (self.tabletop_channel == None):
            await ctx.send("**ERROR**: Tabletop channel not set.")
        else:
            await self.tabletop_channel.send("Test")