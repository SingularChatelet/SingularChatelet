import os
from dotenv import load_dotenv

from pyclass.abstract_bot_app import AbstractBotApp

# Discord Bot
import hikari
from hikari import presences

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]
INTENTS = hikari.Intents.ALL

bot = AbstractBotApp(
    prefix='.',
    token=TOKEN,
    intents=INTENTS,
    logs="ERROR"
)
for file in os.listdir('plugins'):
    if file.endswith('.py'):
        bot.load_extensions(f'plugins.{file[:-3]}')
        print(f'added :: {file}')

bot.run(
    activity=presences.Activity(
        name='with human | /help',
        type=presences.ActivityType.PLAYING
    ),
)
