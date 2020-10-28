from discord.ext import commands

bot = commands.Bot(command_prefix='!')
TOKEN = 'NzY4MTgzOTA0NTIzNjQ5MDQ0.X48xAw.zR3ancojzsaPGsBDfecOmnCoOtM'
cogs_to_add = [
    'cogs.events_watch_cog',
    'cogs.start_deal_cog',
    'cogs.get_fees_cog',
    'cogs.help_cog'
]

if __name__ == "__main__":
    for cog in cogs_to_add:
        print(f'Loading : {cog}')
        bot.load_extension(cog)

bot.run(TOKEN)