import os

from lightbulb import Bot
from lightbulb import slash_commands

class Developper(slash_commands.SlashCommandGroup):
    @property
    def description(self) -> str:
        return "Commands for developpers"

    @property
    def enabled_guilds(self):
        return None

@Developper.subcommand()
class Shutdown(slash_commands.SlashSubCommand):
    @property
    def description(self) -> str:
        return "Close the bot."

    @property
    def options(self):
        return []

    async def callback(self, context: slash_commands.SlashCommandContext) -> None:
        if context.author.id in [606758395583922176, 425965177616334849]:
            context.respond('ok.')
            await context.bot.close()
        else:
            context.respond('only the developpers of this bot can shut down the bot')

def load(bot:Bot):
    bot.add_slash_command(Developper)