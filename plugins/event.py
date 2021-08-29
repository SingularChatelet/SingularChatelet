import lightbulb
from lightbulb.events import CommandErrorEvent
from lightbulb.errors import CommandNotFound

class On_Event(lightbulb.Plugin):

    @lightbulb.listener(CommandErrorEvent)
    async def on_command_error(self, event:CommandErrorEvent):
        if isinstance(event.exception, CommandNotFound):
            if not event.message.content.startswith('..'):
                await event.message.respond('this command dont exists')
        else:
            print(event.exception.with_traceback)

def load(bot:lightbulb.Bot):
    bot.add_plugin(On_Event())