import os
from dotenv import load_dotenv

# Discord Bot
from discord import Intents
from discord.ext.commands import Bot
from discord.ext.commands import when_mentioned_or

from pyclass import send_webhook

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]
PREFIX = when_mentioned_or('.')
INTENTS = Intents.all()

bot = Bot(command_prefix=PREFIX, intents=INTENTS)
bot.chatbot_send = send_webhook.SendWebhook()

for file in os.listdir('cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(TOKEN)