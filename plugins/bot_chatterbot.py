import asyncio
from concurrent.futures import ThreadPoolExecutor

import hikari
from lightbulb import Bot
from lightbulb import slash_commands

class ChatterBot(slash_commands.SlashCommand):
    @property
    def options(self):
        return [
            hikari.CommandOption(
                name="message",
                description="Message to the chatbot.",
                type=hikari.OptionType.STRING,
                is_required=True
            ),
        ]
    
    @property
    def description(self) -> str:
        return "Use chatterbot.corpus.english and ChatterBot to generate response."

    @property
    def enabled_guilds(self):
        return None

    async def callback(self, context:slash_commands.SlashCommandContext) -> None:
        if context.guild_id == None:
            await context.respond('Command only availible on a guild channel')
            return None
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            ThreadPoolExecutor(),
            context.bot._chatterbot_chatbot.get_response,
            context.options['message'].value
        )
        await context.bot._chatbot_send.send(context, str(response), context.options['message'].value)

def load(bot:Bot):
    bot.add_slash_command(ChatterBot)