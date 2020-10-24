from discord.ext import commands
import discord
import asyncio
import requests
import time
from discord import Member
from random import randint
from coinbase_commerce import Client
import os
from bit import Key
class DealCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = Key('5JVy43ya9tYRPP2uuHmfWdazKT8buE31j13ei4p3X1KKpn23Dkx')
        #self.client = Client(api_key=coinbase_api_key)
    def check_addr(self):
        headers = {
            'Authorization': 'Bearer Ugxlr1GIMG5Evu0h9d92oWGho0uwEpg1HW0c3o8Ri1U',
        }

        data = '{"addr":"1NemoJ5zHUvHVApJL7tH47XpM6fMarw94S"}'

        response = requests.post('https://www.blockonomics.co/api/searchhistory', headers=headers, data=data)
        return response.json()
    @commands.command()
    async def tdeal(self, ctx, member : Member, *, rest):
        #if member.id == ctx.author.id:
        #=#    await ctx.send('You cannot middleman a deal you have made with yourself.')
        #    return
        guild = ctx.guild
        print(rest)
        auth = ctx.author


        headers = {'accept': 'application/json',}
        params = (('ids', 'bitcoin'),('vs_currencies', 'usd'),)
        btc_price = requests.get('https://api.coingecko.com/api/v3/simple/price', headers=headers, params=params)
        btc_price = btc_price.json()
        btc_price = btc_price['bitcoin']['usd']
        satoshi_price = btc_price * 100_000_000
        r= requests.get('https://bitcoinfees.earn.com/api/v1/fees/recommended')
        resp = r.json()
        embed = discord.Embed(title='Fees', description='We get our fees from bitcoinfees.com and we expect the size of the transaction to be roughly between 300 and 400 bytes so we use this to calculate the fee in usd. Though you can set a custom fee it is not recommended and if the fees dont come through for a long time then we cannot assist you with that.\n\n'\
            f'That being said, here are the current fees\n 🅰️ Fastest : {resp["fastestFee"]}s/b = **${round(btc_price * ((resp["fastestFee"] / 100_000_000)*400),2)}**\n'\
                f'🅱️ Half hour fee : {resp["halfHourFee"]}s/b = **${round(btc_price * ((resp["halfHourFee"] / 100_000_000) * 400),2)}**\n'\
                    f'⏭️ One hour fee {resp["hourFee"]}s/b = **${round(btc_price * ((resp["hourFee"] / 100_000_000) * 400), 2)}**\n'\
                        f'👌 Custom fee')
        sent = await ctx.send(embed=embed)
        await sent.add_reaction('🅰️')
        await sent.add_reaction('🅱️')
        await sent.add_reaction('⏭️')
        await sent.add_reaction('👌')
        def check(reaction, user):
            return user.id != 768183904523649044
        response = await self.bot.wait_for('reaction_add',check=check)
        if response[0].emoji == '🅰️':
            print(resp)
            print(resp['fastestFee'])
            fee = resp['fastestFee']
        elif response[0].emoji == '🅱️':
            fee = resp['halfHourFee']
        elif response[0].emoji == '⏭️':
            fee = response['hourFee']
        elif response[0].emoji == '👌':
            await ctx.send('Please send the amount in satoshis/byte `https://www.buybitcoinworldwide.com/fee-calculator/` look here for reference, please only send a number')
        def check(message):
            try:
                int(message.content)
                print('accepted')
            except Exception as e:
                return False
                print(e)
            return True
                    
        resp = await self.bot.wait_for('message', check=check)
        fee = int(resp.content)

        rest = int(rest)
        my_fee = (rest / 100) * 2.5
        to_send = rest - my_fee
        addy = self.key.address
        output = [(addy, 1, 'usd')]
        money_out = self.key.send(output, fee=fee)
        await ctx.send(f'Thank you for using middler bot, ${to_send} has been sent to {addy} view it here : https://www.blockchain.com/btc/tx/{money_out} if the transaction fee is massively under what you paid please contact support server @ https://discord.gg/9yuDE5u')
        await ctx.send(f'This bot was made by xo#0111 :) ')
        log = self.bot.get_channel(768937585434427404)
        await log.send(f'New deal\nSeller : \nBuyer: \nValue: {rest}\nFINAL_TX : {money_out}')
        await ctx.send('This ctx will be deleted in 60 seconds')
        await asyncio.sleep(60)

                #r = self.key.create_transaction([addy, int(rest), 'usd'], fee=22000)


                #Ugxlr1GIMG5Evu0h9d92oWGho0uwEpg1HW0c3o8Ri1U
        #ctx = await guild.create_text_ctx('secret', overwrites=overwrites)
        #await ctx.send('Deal has been setup')

def setup(bot):
    bot.add_cog(DealCog(bot))