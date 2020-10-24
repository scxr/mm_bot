from discord.ext import commands
import discord
import requests
class GetFees(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def fees(self, ctx):
        r= requests.get('https://bitcoinfees.earn.com/api/v1/fees/recommended')
        resp = r.json()
        embed = discord.Embed(title='Fees', description='We get our fees from bitcoinfees.com and we expect the size of the transaction to be roughly between 300 and 400 bytes so we use this to calculate the fee in usd. Though you can set a custom fee it is not recommended and if the fees dont come through for a long time then we cannot assist you with that.\n\n'\
            f'That being said, here are the current fees\n 🅰️ Fastest : {resp["fastestFee"]}s/b\n'\
                f'🅱️ Half hour fee : {resp["halfHourFee"]}s/b\n'\
                    f'⏭️ One hour fee {resp["hourFee"]}s/b\n')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GetFees(bot))