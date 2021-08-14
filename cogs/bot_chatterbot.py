from discord.ext import commands

import asyncio
from concurrent.futures import ThreadPoolExecutor

# ChatBot
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class Bot_ChatterBot(commands.Cog):
    def __init__(self, bot:commands.Bot):
        """Cogs related to ChatterBot lib."""
        self.bot:commands.Bot = bot
        self._chatbot = ChatBot(
            name='SingularChatelet',
            read_only=False,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri='sqlite:///data/chatterbot/db.sqlite3',
            logic_adaptaters=[
                'chatterbot.logic.BestMatch',
            ]
        )
        trainer_corpus = ChatterBotCorpusTrainer(self._chatbot, show_training_progress=False)
        trainer_corpus.train('chatterbot.corpus.english')
        print("Bot_ChatterBot init ready!")

    @commands.guild_only()
    @commands.command(aliases=['chatterbot'])
    async def cb(self, ctx:commands.Context, *,sentence):
        """Use chatterbot.corpus.english and ChatterBot to generate response."""
        async with ctx.typing():
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                ThreadPoolExecutor(),
                self._chatbot.get_response,
                sentence
            )
            await self.bot.chatbot_send.send(ctx, str(response))


def setup(bot:commands.Bot):
    bot.add_cog(Bot_ChatterBot(bot))
