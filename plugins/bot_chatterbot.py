import asyncio
from concurrent.futures import ThreadPoolExecutor

import hikari
from lightbulb import Bot
from lightbulb import slash_commands

class ChatterBot(slash_commands.SlashCommand):
    description="Use chatterbot.corpus.english and ChatterBot to generate response."
    # Options:
    message : str = slash_commands.Option(
        description="Message to the chatbot.",
        required=True
    )

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