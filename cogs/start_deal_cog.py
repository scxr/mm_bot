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
        self.key = Key('5J56DguGRz1hpbzT9E5KFMhuMZVf16EfGKYB5JkM2eKgsHRsSJE')
        #self.client = Client(api_key=coinbase_api_key)
    def check_addr(self):
        headers = {
            'Authorization': 'Bearer Ugxlr1GIMG5Evu0h9d92oWGho0uwEpg1HW0c3o8Ri1U',
        }

        data = '{"addr":"1mid3EoZEkDbHsNvNKc9UscXSn2ZgGK2Q"}'

        response = requests.post('https://www.blockonomics.co/api/searchhistory', headers=headers, data=data)
        return response.json()
    @commands.command()
    async def deal(self, ctx, member : Member, *, rest):
        if member.id == ctx.author.id:
            await ctx.send('You cannot middleman a deal you have made with yourself.')
            return
        guild = ctx.guild
        print(rest)
        auth = ctx.author
        try:
            rest = int(rest)
        except:
            await ctx.send(f'{rest} is not a valid number')
            return
        overwrites = {
            guild.default_role : discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True, read_message_history=True),
            member: discord.PermissionOverwrite(read_messages=True, read_message_history=True),
            auth : discord.PermissionOverwrite(read_messages=True, read_message_history=True) 
        }
        embed = discord.Embed(title='New deal', description=f'{member.mention} the user {ctx.author.mention} is trying to start a deal\nPlease type either `confirm` or `deny`', colour=randint(0, 0xffffff))
        await ctx.send(embed=embed)
        
        try:    
            msg = await self.bot.wait_for('message', check=lambda message: message.author == member, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send('User failed to respond within 60 seconds. Closing deal')
        if msg.content.lower() == 'confirm':
            #support = discord.ChannelPermissions(target=discord.utils.get(ctx.message.server.roles, name=config_setup.support_role), overwrite=support_perms)
            channel = await guild.create_text_channel(f'{auth.id + member.id}', overwrites=overwrites)
            await ctx.send(f'Channel set up : {channel.mention}')
            deal_embed = discord.Embed(title='Deal setup', description=f'A deal for ${rest} has been setup, if you are happy for me to hold this in escrow react with ✅ to cancel this deal please react with ❌', colour=randint(0, 0xffffff))
            sent = await channel.send(embed=deal_embed)
            await sent.add_reaction('✅')
            await sent.add_reaction('❌')
            def check(reaction, user):
                return reaction.message.id == sent.id and user.id != 768183904523649044
            

            response = await self.bot.wait_for('reaction_add', check=check)
            print(response)
            print(response[0].emoji)
            if response[0].emoji == '❌':
                await channel.delete()
            if response[0].emoji == '✅':
                embed = discord.Embed(title='Who is who?', description='If you are the seller please react to this with 💼 to cancel the deal react with ❌')
                sent = await channel.send(embed=embed)
                await sent.add_reaction('💼')
                await sent.add_reaction('❌')
                def check(reaction, user):
                    return user.id == auth.id or user.id == member.id

                resp = await self.bot.wait_for('reaction_add', check=check)

                if resp[0].emoji == '❌':
                    await channel.send('Closing deal')
                    await channel.delete()
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
                response = await self.bot.wait_for('reaction_add',check=check)
                if response[0].emoji == '✅':
                    pass
                elif response[0].emoji == '❌':
                    if seller.id == member.id:
                        seller = auth
                        buyer = member
                    else:
                        seller = member
                        buyer = auth
                else:
                    await channel.send('Cancelling deal')
                    await channel.delete()
                    return
                #resp = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
                #btc_price = 

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
                sent = await channel.send(embed=embed)
                await sent.add_reaction('🅰️')
                await sent.add_reaction('🅱️')
                await sent.add_reaction('⏭️')
                await sent.add_reaction('👌')
                def check(reaction, user):
                    return user.id != 768183904523649044
                response = await self.bot.wait_for('reaction_add',check=check)
                if response[0].emoji == '🅰️':

                    fee = resp['fastestFee']
                elif response[0].emoji == '🅱️':
                    fee = resp['halfHourFee']
                elif response[0].emoji == '⏭️':
                    fee = response['hourFee']
                elif response[0].emoji == '👌':
                    await channel.send('Please send the amount in satoshis/byte `https://www.buybitcoinworldwide.com/fee-calculator/` look here for reference, please only send a number')
                    def check(message):
                        try:
                            int(message.content)
                        except:
                            return False
                        return True
                    
                    resp = await self.bot.wait_for('message', check=check)
                    fee = int(resp.content)

                #https://bitcoinfees.earn.com/api/v1/fees/recommended
                fee_btc = (fee / 100_000_000) * 400
                print(fee_btc, type(fee_btc))
                fee_usd = btc_price * fee_btc
                req_money = discord.Embed(
                    title='Send funds!',
                    description=f'{buyer.mention} Please send **__exactly__** **${rest}** + fee set above **(${round(int(rest)+fee_usd, 2)})** or **{(1/btc_price) * (rest+3) + fee_btc}** BTC to **{self.key.address}**\n'\
                        'We are monitoring for the transaction now. We will stop waiting after 30 minutes. If you have not sent exactly the correct amount it will not be detected (We check for new transactions every 5 minutes, so if its a bit slow, dont worry).\n If you have made an error please join the support server: https://discord.gg/9yuDE5u',
                    colour=randint(0, 0xFFFFFF)
                )

                #r = requests.get(f'https://api.blockcypher.com/v1/btc/main/txs/{tx}') 
                await channel.send(embed=req_money)
                cnt = 0
                done = False
                while 1:
                    transactions = self.check_addr()
                    print(transactions)
                    print(transactions["pending"])
                    if len(transactions["pending"]) > 0:
                        tx = transactions["pending"][0]["txid"]
                        for i in transactions["pending"]:
                            if i["value"] < 0:
                                value = i["value"] * -1
                                print(value/ 100_000_000)
                                if value / 100_000_000 >= (1/btc_price) * (rest+fee_btc) <= (1/btc_price * ((rest+3) + 10)):
                                    embed = discord.Embed(title=f'New transaction detected of {i["value"] /100_000_000} BTC recieved', description='We will now wait for the funds to be confirmed at least once')
                                    await channel.send(embed=embed)
                                    done = True
                            if i["value"] / 100_000_000 >= (1/btc_price) * (rest+3) <= (1/btc_price * ((rest+3) + 10)):

                                embed = discord.Embed(title=f'New transaction detected of {i["value"] /100_000_000} BTC recieved', description='We will now wait for the funds to be confirmed at least once')
                                await channel.send(embed=embed)
                                done = True
                        if done==True:
                            break
                    elif cnt == 6:
                        embed = discord.Embed(title='It has been 30 minutes', description='No transaction detected in 30 minutes, cancelling deal.')
                        await channel.send(embed=embed)
                        await asyncio.sleep(30)
                        await channel.delete()
                        return
                    await asyncio.sleep(300)
                print('here')
                cnt = 0
                while 1:
                    r = requests.get(f'https://www.blockonomics.co/api/tx_detail?txid={tx}')
                    rjs = r.json()
                    print(rjs)
                    if str(rjs["status"]) != "0" and str(rjs['status']) != 'Unconfirmed':
                        print(rjs["status"])
                        embed = discord.Embed(title='Fees have been confirmed', description='The fees have at least one confirm, the deal can proceed')
                        await channel.send(embed=embed)
                        break
                        
                    await asyncio.sleep(300)
                    cnt += 1
                    if cnt == 24:
                        embed = discord.Embed(title='Timed out', description='It has been 2 hours and no confirmations, I will assume they have been double spent. If this is incorrect please contact the support server here : https://discord.gg/9yuDE5u', colour=randint(0, 0xFFFFFF))
                        await channel.send(embed=embed)

                        return
                embed = discord.Embed(title='Transfer the goods', description=f'{seller.mention} Please could you send the instructions to secure the account. Once you have secured {buyer.mention} please type `confirm` if something has gone wrong please join the support server and open a ticket @ https://discord.gg/9yuDE5u', colour=0x00FF00)
                await channel.send(embed=embed)
                def check(message):
                    return message.author.id == buyer.id and message.content == 'confirm'
                
                resp = await self.bot.wait_for('message', check=check)
                await channel.send(f'{seller.mention} please send your btc address **__NOTHING EXTRA__**')
                def check(message):
                    return message.author.id == seller.id
                
                resp = await self.bot.wait_for('message', check=check)
                addy = resp.content
                while 1:
                    r = requests.get(f'https://www.blockonomics.co/api/tx_detail?txid={tx}')
                    rjs = r.json()
                    print(rjs)
                    if rjs['status'] != 'Confirmed':
                        await channel.send(f'The fees have not been fully transferred yet, current status : {rjs["status"]} the funds will be released to {addy} once it is fully confirmed')
                    else:
                        break
                    await asyncio.sleep(300)



                rest = int(rest)
                my_fee = (rest / 100) * 2.5
                to_send = rest - my_fee
                addy = self.key.address
                output = [(addy, to_send, 'usd')]
                money_out = self.key.send(output, fee=fee)
                await channel.send(f'Thank you for using middler bot, ${to_send} has been sent to {addy} view it here : https://www.blockchain.com/btc/tx/{money_out} if the transaction fee is massively under what you paid please contact support server @ https://discord.gg/9yuDE5u')
                await channel.send(f'This bot was made by xo#0111 :) ')
                log = self.bot.get_channel(768937585434427404)
                await log.send(f'New deal\nSeller : {seller.id}\nBuyer: {buyer.id}\nValue: {rest}\nFINAL_TX : {money_out}')
                await channel.send('This channel will be deleted in 60 seconds')
                await asyncio.sleep(60)
                await channel.delete()
                #r = self.key.create_transaction([addy, int(rest), 'usd'], fee=22000)


                #Ugxlr1GIMG5Evu0h9d92oWGho0uwEpg1HW0c3o8Ri1U
        #channel = await guild.create_text_channel('secret', overwrites=overwrites)
        #await channel.send('Deal has been setup')

def setup(bot):
    bot.add_cog(DealCog(bot))
