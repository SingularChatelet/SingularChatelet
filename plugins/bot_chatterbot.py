import asyncio
from concurrent.futures import ThreadPoolExecutor

from pyclass.abstract_bot_app import AbstractBotApp as Bot
import lightbulb

plugin = lightbulb.Plugin("ChatterBot")

@plugin.command
@lightbulb.option("message", "the message", required=True)
@lightbulb.command("chatterbot", "Use chatterbot.corpus.english and ChatterBot to generate response.")
@lightbulb.implements(lightbulb.SlashCommand)
async def smth(context: lightbulb.Context) -> None:
    if context.guild_id == None:
        await context.respond('Command only availible on a guild channel')
        return None
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        ThreadPoolExecutor(),
        context.bot._chatterbot_chatbot.get_response,
        context.options['message']
    )
    await context.bot._chatbot_send.send(context, str(response), context.options['message'])

def load(bot:Bot):
    if bot._full_bot_chatterbot == False:
        return None
    bot.add_plugin(plugin)
