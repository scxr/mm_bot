from discord.ext import commands

bot = commands.Bot(command_prefix='!')
TOKEN = 'NzY3NzIxMTUyMDc2MTg1NjAw.X42CCg.BGUsEXq_kaFJxxlGmIVqV0dfvYE'
cogs_to_add = [
    'cogs.hello_world',
    'cogs.events_watch_cog',
    'cogs.start_deal_cog'
]

if __name__ == "__main__":
    for cog in cogs_to_add:
        print(f'Loading : {cog}')
        bot.load_extension(cog)

bot.run(TOKEN)