from discord.ext import commands

class EventsWatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')

def setup(bot):
    bot.add_cog(EventsWatch(bot))