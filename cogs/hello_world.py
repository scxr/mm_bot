from discord.ext import commands

class hello_world(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def hello_world(self, ctx):
        await ctx.send('hello world')

def setup(bot):
    bot.add_cog(hello_world(bot))