import os

# Discord Bot
from discord import Intents
from discord.ext.commands import Bot
from discord.ext.commands import when_mentioned_or

TOKEN = "NzEwNDA3MjY0MDcwMTM5OTQ0.Xr0AUg.o2hFHXFOamuFBJdmSMj0-Tp159A"#os.environ["DISCORD_TOKEN"]
PREFIX = when_mentioned_or('.')
INTENTS = Intents.all()

bot = Bot(command_prefix=PREFIX, intents=INTENTS)

for file in os.listdir('cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(TOKEN)