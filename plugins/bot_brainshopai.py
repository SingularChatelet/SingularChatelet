import os
import requests
import urllib.parse

import asyncio
from concurrent.futures import ThreadPoolExecutor

import hikari
from lightbulb import Bot
from lightbulb import slash_commands

class BrainShopAI(slash_commands.SlashCommand):
    description="Use brainshopAI api to generate a response."
    # Options:
    message : str = slash_commands.Option(
        description="the message",
        required=True
    )

    async def callback(self, context: slash_commands.SlashCommandContext) -> None:
        if context.guild_id == None:
            await context.respond('Command only availible on a guild channel')
            return None
        msg = urllib.parse.quote_plus(context.options['message'].value)
        bid = os.environ.get("BRAINSHOP_BID", None)
        if bid == None:
            print("You need to sign in to brainshop.ai and get your bid")
            await context.respond('Could not execute this command')
            return None
        key = os.environ.get('BRAINSHOP_KEY', None)
        if key == None:
            print("You need to sign in to brainshop.ai and get your api key")
            await context.respond('Could not execute this command')
            return None
        uid = context.author.id
        url = f"http://api.brainshop.ai/get?bid={bid}&key={key}&uid={uid}&msg={msg}"
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            ThreadPoolExecutor(),
            requests.get,
            url
        )
        resp = await loop.run_in_executor(
            ThreadPoolExecutor(),
            result.json
        )
        if 'cnt' not in resp.keys():
            await context.respond(f'bad result : {resp}')
            return None
        await context.bot._chatbot_send.send(context, str(resp['cnt']), context.options['message'].value)

def load(bot:Bot):
    bot.add_slash_command(BrainShopAI)