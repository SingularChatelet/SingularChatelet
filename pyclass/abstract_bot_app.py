import lightbulb
from .send_webhook import SendWebhook

try:
    from transformers import AutoTokenizer
    from transformers import AutoModelForCausalLM
    import torch
    full_bot_transformers = True
except ModuleNotFoundError:
    full_bot_transformers = False

try:
    from chatterbot import ChatBot
    from chatterbot.trainers import ChatterBotCorpusTrainer
    full_bot_chatterbot = True
except ModuleNotFoundError:
    full_bot_chatterbot = False

class AbstractBotApp(lightbulb.BotApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._chatbot_send = SendWebhook()
        self._full_bot_transformers = full_bot_transformers
        if full_bot_transformers == True:
            # Transformers
            # pre_trained possibility : microsoft/DialoGPT-large | microsoft/DialoGPT-medium | microsoft/DialoGPT-small
            self._transformers_tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small", cache_dir='./data/transformers/')
            self._transformers_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small", cache_dir='./data/transformers/')
            self._transformers_conversations = {}
        self._full_bot_chatterbot = full_bot_chatterbot
        if full_bot_chatterbot == True:
            # ChatterBot
            self._chatterbot_chatbot = ChatBot(
                name='SingularChatelet',
                read_only=False,
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database_uri='sqlite:///data/chatterbot/db.sqlite3',
                logic_adaptaters=[
                    'chatterbot.logic.BestMatch',
                ]
            )
            trainer_corpus = ChatterBotCorpusTrainer(self._chatterbot_chatbot, show_training_progress=False)
            trainer_corpus.train('chatterbot.corpus.english')
