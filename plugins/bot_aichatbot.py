import os
import requests

import asyncio
from concurrent.futures import ThreadPoolExecutor

import hikari
from pyclass.abstract_bot_app import AbstractBotApp as Bot
import lightbulb

plugin = lightbulb.Plugin("Aichatbot")

def requests_abstract(url, headers, querystring):
    """abstract the requests call"""
    res = requests.request("GET", url, headers=headers, params=querystring)
    return res

@plugin.command
@lightbulb.option("message", "the message", required=True)
@lightbulb.command("aichatbot", "Use aichatbot api to generate a response.")
@lightbulb.implements(lightbulb.SlashCommand)
async def smth(context: lightbulb.Context) -> None:
    if context.guild_id == None:
        await context.respond('Command only availible on a guild channel')
        return None
    url = "https://ai-chatbot.p.rapidapi.com/chat/free"
    sentence = context.options['message']
    uid = str(context.author.id)
    querystring = {"message":sentence, "uid":uid}
    key = os.environ.get('RAPID_API_KEY', None)
    if key == None:
        print('please provide a rapidapi key and subscribe to simsimi api')
        await context.respond('Could not execute this command')
        return None
    headers = {
        'x-rapidapi-host': "ai-chatbot.p.rapidapi.com",
        'x-rapidapi-key': key
    }
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        ThreadPoolExecutor(),
        requests_abstract,
        url, headers, querystring
    )
    resp = result.json()
    resp = resp.get('chatbot', None)
    if resp == None:
        print(result.text)
        await context.respond('could not execute this command')
        return None
    msg = resp.get('response', None)
    if msg == None:
        print(result.text)
        await context.respond('Could not execute this command')
        return None
    await context.bot._chatbot_send.send(context, msg, sentence)
    return None

def load(bot:Bot):
    bot.add_plugin(plugin)
