from discord.ext import commands
import discord
import asyncio
from discord import Member
from random import randint
from coinbase_commerce import Client
import os

class DealCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.priv_key = os.getenv('private_key')
        #self.client = Client(api_key=coinbase_api_key)
    
    @commands.command()
    async def deal(self, ctx, member : Member, *, rest):
        guild = ctx.guild
        print(rest)
        #auth = ctx.author
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            member: discord.PermissionOverwrite(read_messages=True)
        }
        embed = discord.Embed(title='New deal', description=f'{member.mention} the user {ctx.author.mention} is trying to start a deal\nPlease type either `!confirm` or `!deny`', colour=randint(0, 0xffffff))
        await ctx.send(embed=embed)
        try:    
            msg = await self.bot.wait_for('message', check=lambda message: message.author == member, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send('User failed to respond within 60 seconds. Closing deal')
        if msg.content.lower() == '!confirm':
            channel = await guild.create_text_channel(f'{member.id+ctx.author.id}', overwrites=overwrites)
            await ctx.send(f'Channel has been setup, please go to {channel.mention}', delete_after=60)
            deal_embed = discord.Embed(title='Deal setup', description=f'A deal for ${rest} has been setup, if you are happy for me to hold this in escrow react with ✅ to cancel this deal please react with ❌', colour=randint(0, 0xffffff))
            sent = await channel.send(embed=deal_embed)
            await sent.add_reaction('✅')
            await sent.add_reaction('❌')
            def check(reaction, user):
                return reaction.message.id == sent.id and user.id != 767721152076185600
            

            response = await self.bot.wait_for('reaction_add', check=check)
            print(response[0].emoji)
            await channel.send('ok')
        #channel = await guild.create_text_channel('secret', overwrites=overwrites)
        #await channel.send('Deal has been setup')

def setup(bot):
    bot.add_cog(DealCog(bot))