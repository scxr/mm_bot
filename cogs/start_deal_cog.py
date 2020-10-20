from discord.ext import commands
import discord
import asyncio
from discord import Member
from random import randint
#from coinbase_commerce import Client
import os

class DealCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.priv_key = os.getenv('private_key')
        #self.client = Client(api_key=coinbase_api_key)
    
    @commands.command()
    async def deal(self, ctx, member : Member, *, rest):
        guild = ctx.guild
        print(rest)
        auth = ctx.author
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            member: discord.PermissionOverwrite(read_messages=True)
        }
        embed = discord.Embed(title='New deal', description=f'{member.mention} the user {ctx.author.mention} is trying to start a deal\nPlease type either `confirm` or `deny`', colour=randint(0, 0xffffff))
        await ctx.send(embed=embed)
        try:    
            msg = await self.bot.wait_for('message', check=lambda message: message.author == member, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send('User failed to respond within 60 seconds. Closing deal')
        if msg.content.lower() == 'confirm':
            channel = await guild.create_text_channel(f'{member.id+ctx.author.id}', overwrites=overwrites)
            await ctx.send(f'Channel has been setup, please go to {channel.mention}', delete_after=60)
            deal_embed = discord.Embed(title='Deal setup', description=f'A deal for ${rest} has been setup, if you are happy for me to hold this in escrow react with ✅ to cancel this deal please react with ❌', colour=randint(0, 0xffffff))
            sent = await channel.send(embed=deal_embed)
            await sent.add_reaction('✅')
            await sent.add_reaction('❌')
            def check(reaction, user):
                return reaction.message.id == sent.id and user.id != 768183904523649044
            

            response = await self.bot.wait_for('reaction_add', check=check)
            print(response)
            print(response[0].emoji)
            if response[0].emoji == '✅':
                embed = discord.Embed(title='Who is who?', description='If you are the seller please react to this with 💼 to cancel the deal react with ❌')
                sent = await channel.send(embed=embed)
                await sent.add_reaction('💼')
                await sent.add_reaction('❌')
                def check(reaction, user):
                    return user.id == auth.id or user.id == member.id

                resp = await self.bot.wait_for('reaction_add', check=check)

                if resp[0].emoji == '❌':
                    await ctx.send('Closing deal')
                    return
                elif resp[0].emoji == '💼':
                    if resp[1].id == auth.id:
                        seller = auth
                        buyer = member
                    else:
                        seller = member
                        buyer = auth
                embed = discord.Embed(title='Just checking', description=f'Just checking that {seller.mention} is the seller and that {buyer.mention} is the buyer\n'\
                'React with ✅ to confirm this info, React with ❌ if this is incorrect, React with 🛑 to cancel the deal ')
                sent = await channel.send(embed=embed)
                await sent.add_reaction('✅')
                await sent.add_reaction('❌')
                await sent.add_reaction('🛑')
                def check(reaction, user):
                    return user.id != 768183904523649044
                resp = await self.bot.wait_for('reaction_add',check=check)
                if resp[0].emoji == '✅':
                    pass
                elif resp[0].emoji == '❌':
                    if seller.id == member.id:
                        seller = auth
                        buyer = member
                    else:
                        seller = member
                        buyer = auth
                else:
                    await channel.send('Cancelling deal')
                
                req_money = discord.Embed(
                    title='Send funds!',
                    description=f'{buyer.mention} Please send exactly **${rest}** + 3$ (${int(rest)+3}) to **5JVy43ya9tYRPP2uuHmfWdazKT8buE31j13ei4p3X1KKpn23Dkx**\n'\
                        'Once sent please send the TX (can be url or regular TX) then we will wait for 1 confirmation, to cancel the deal reply to this with `cancel`',
                    colour=randint(0, 0xFFFFFF)
                )

                await ctx.send(embed=Embed)
                def check(message):
                    return message.author.id == buyer.id
                resp = await self.bot.wait_for('message', check=check)
                if 'cancel' in resp.content.lower():
                    await channel.send(f'{buyer.mention} cancelled the deal')
                    return
                else:
                    tx = resp.content
                    r = requests.get(f'https://api.blockcypher.com/v1/btc/main/txs/{tx}') 
                    print(r.json)

        #channel = await guild.create_text_channel('secret', overwrites=overwrites)
        #await channel.send('Deal has been setup')

def setup(bot):
    bot.add_cog(DealCog(bot))