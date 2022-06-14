import os
from time import sleep

import hikari
from pyclass.abstract_bot_app import AbstractBotApp as Bot
import lightbulb

plugin = lightbulb.Plugin("Developper")

@plugin.command
@lightbulb.command("developpers", "Commands for the developpers")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def parent(context: lightbulb.Context) -> None:
    await context.respond("Use the subcommands for developpers purpose")

@parent.child
@lightbulb.command("shutdown", "close the bot")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def bot_func_bot(context: lightbulb.Context) -> None:
    if context.author.id in [606758395583922176, 425965177616334849]:
        await context.respond('ok.')
        sleep(2)
        await context.bot.close()
    else:
        await context.respond('only the developpers of this bot can shut down the bot')

def load(bot:Bot):
    bot.add_plugin(plugin)
