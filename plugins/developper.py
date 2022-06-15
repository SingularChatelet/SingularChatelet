import os
from time import sleep

try:
    from transformers import AutoTokenizer
    from transformers import AutoModelForCausalLM
    transformers_availible = True
except ModuleNotFoundError:
    transformers_availible = False

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

if transformers_availible == True:
    @parent.child
    @lightbulb.command("re_init_transformers_data", "If the data is corumpted by bias, re init the data.")
    @lightbulb.implements(lightbulb.SlashSubCommand)
    async def bot_func_rem(context: lightbulb.Context) -> None:
        if context.author.id not in [606758395583922176, 425965177616334849]:
            await context.respond('only the developpers of this bot can shut down the bot')
        for file in os.listdir('./data/transformers'):
            if not file.endswith('.txt'):
                os.remove(f'data/transformers/{file}')
        await context.respond('remove all file.. Now donwloading..')
        context.bot._transformers_tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/DialoGPT-large",
            cache_dir='./data/transformers/'
        )
        context.bot._transformers_model = AutoModelForCausalLM.from_pretrained(
            "microsoft/DialoGPT-large",
            cache_dir='./data/transformers/'
        )
        channel = context.get_channel()
        await context.bot.rest.create_message(channel=channel, content='Download finish! All data were re init')

def load(bot:Bot):
    bot.add_plugin(plugin)
