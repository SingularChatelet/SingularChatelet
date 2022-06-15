import lightbulb
from lightbulb.events import CommandErrorEvent
from lightbulb.errors import CommandNotFound

from pyclass.abstract_bot_app import AbstractBotApp as Bot

plugin = lightbulb.Plugin("Events")

@plugin.listener(CommandErrorEvent)
async def smth(event: CommandErrorEvent) -> None:
    if isinstance(event.exception, CommandNotFound):
        await event.context.respond('this command dont exists')
    else:
        await event.context.respond(f"{event.exception}")

def load(bot: Bot):
    bot.add_plugin(plugin)
