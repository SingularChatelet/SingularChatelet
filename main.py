import os
from dotenv import load_dotenv

from pyclass import send_webhook

# Discord Bot
import hikari
import lightbulb
from hikari import presences

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]
INTENTS = hikari.Intents.ALL

bot = lightbulb.Bot(
    prefix='.',
    token=TOKEN,
    intents=INTENTS,
    logs="ERROR"
)
bot._chatbot_send = send_webhook.SendWebhook()

for file in os.listdir('plugins'):
    if file.endswith('.py'):
        bot.load_extension(f'plugins.{file[:-3]}')
        print(f'added :: {file}')

bot.run(
    activity=presences.Activity(
        name='with human | /help',
        type=presences.ActivityType.PLAYING
    ),
)