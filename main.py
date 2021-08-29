import os
from importlib import import_module
from dotenv import load_dotenv

from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

from pyclass import send_webhook

# Discord Bot
import hikari
import lightbulb

load_dotenv()

TOKEN = os.environ["DISCORD_TOKEN"]
INTENTS = hikari.Intents.ALL

bot = lightbulb.Bot(prefix='.', token=TOKEN, intents=INTENTS, logs="ERROR")
bot._chatbot_send = send_webhook.SendWebhook()
# Transformers
# pre_trained possibility : microsoft/DialoGPT-large | microsoft/DialoGPT-medium | microsoft/DialoGPT-small
bot._transformers_tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small", cache_dir='./data/transformers/')
bot._transformers_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small", cache_dir='./data/transformers/')
bot._transformers_conversations = {}
# ChatterBot
bot._chatterbot_chatbot = ChatBot(
    name='SingularChatelet',
    read_only=False,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///data/chatterbot/db.sqlite3',
    logic_adaptaters=[
        'chatterbot.logic.BestMatch',
    ]
)
trainer_corpus = ChatterBotCorpusTrainer(bot._chatterbot_chatbot, show_training_progress=False)
trainer_corpus.train('chatterbot.corpus.english')

for file in os.listdir('./slash_plugins'):
    if file.endswith('.py'):
        bot.load_extension(f'slash_plugins.{file[:-3]}')
        print(f'added :: {file}')

bot.run()