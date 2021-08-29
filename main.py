import os
from importlib import import_module
from dotenv import load_dotenv

# Discord Bot
import hikari
import lightbulb


from pyclass import send_webhook
from plugins import bot_aichatbot

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]
INTENTS = hikari.Intents.ALL

bot = lightbulb.Bot(prefix='.', token=TOKEN, intents=INTENTS)
bot._chatbot_send = send_webhook.SendWebhook()

bot.add_slash_command(bot_aichatbot.Aichatbot)

bot.run()