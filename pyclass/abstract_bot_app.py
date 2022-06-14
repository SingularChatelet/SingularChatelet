import lightbulb
from .send_webhook import SendWebhook

class AbstractBotApp(lightbulb.BotApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._chatbot_send = SendWebhook()
