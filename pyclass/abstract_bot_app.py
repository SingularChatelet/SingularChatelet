import lightbulb
from .send_webhook import SendWebhook

from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class AbstractBotApp(lightbulb.BotApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._chatbot_send = SendWebhook()
        # Transformers
        # pre_trained possibility : microsoft/DialoGPT-large | microsoft/DialoGPT-medium | microsoft/DialoGPT-small
        self._transformers_tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small", cache_dir='./data/transformers/')
        self._transformers_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small", cache_dir='./data/transformers/')
        self._transformers_conversations = {}
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
