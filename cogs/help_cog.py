from discord.ext import commands
import discord
from random import randint
class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')
    
    @commands.command()
    async def help(self, ctx):
        help_embed = discord.Embed(title='Help!', colour=randint(0,0xFFFFFF))
        help_embed.add_field(name='Start A Deal', value='`!deal @member value` Please note, value must be an integer with no dollar sign or anything after', inline=False)
        help_embed.add_field(name='View current transaction fees', value='`!fees` This shows current recommended transaction fees fetched from : `https://bitcoinfees.earn.com/api/v1/fees/recommended`', inline=False)
        help_embed.set_footer(text='Made by xo#0111')
        await ctx.send(embed=help_embed)

def setup(bot):
    bot.add_cog(HelpCog(bot))
