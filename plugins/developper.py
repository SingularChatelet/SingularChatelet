import os

from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

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

@Developper.subcommand()
class Re_Init_Transformers_data(slash_commands.SlashSubCommand):
    @property
    def options(self):
        return []

    @property
    def description(self) -> str:
        return "If the data is corumpted by bias, re init the data."

    async def callback(self, context: slash_commands.SlashCommandContext) -> None:
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
        channel = context.channel
        await context.bot.rest.create_message(channel=channel, content='Download finish! All data were re init')

def load(bot:Bot):
    bot.add_slash_command(Developper)