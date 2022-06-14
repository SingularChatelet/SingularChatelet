import os
import requests
import urllib.parse

import asyncio
from concurrent.futures import ThreadPoolExecutor

import hikari
from pyclass.abstract_bot_app import AbstractBotApp as Bot
import lightbulb

plugin = lightbulb.Plugin("BrainShopAI")

@plugin.command
@lightbulb.option("message", "the message", required=True)
@lightbulb.command("brainshopai", "Use aichatbot api to generate a response.")
@lightbulb.implements(lightbulb.SlashCommand)
async def smth(context: lightbulb.Context) -> None:
    if context.guild_id == None:
        await context.respond('Command only availible on a guild channel')
        return None
    msg = urllib.parse.quote_plus(context.options['message'])
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
    await context.bot._chatbot_send.send(context, str(resp['cnt']), context.options['message'])

def load(bot:Bot):
    bot.add_plugin(plugin)
