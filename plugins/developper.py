import os
from time import sleep

from lightbulb import Bot
from lightbulb import slash_commands

class Developper_Only(slash_commands.SlashCommandGroup):
    description="Commands for the developpers"

@Developper_Only.subcommand()
class Shutdown(slash_commands.SlashSubCommand):
    description="Close the bot."

    async def callback(self, context: slash_commands.SlashCommandContext) -> None:
        if context.author.id in [606758395583922176, 425965177616334849]:
            await context.respond('ok.')
            sleep(2)
            await context.bot.close()
        else:
            await context.respond('only the developpers of this bot can shut down the bot')

def load(bot:Bot):
    bot.add_slash_command(Developper_Only)