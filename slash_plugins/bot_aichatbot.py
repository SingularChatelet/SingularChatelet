import os
import requests

import asyncio
from concurrent.futures import ThreadPoolExecutor

import hikari
from lightbulb import Bot
from lightbulb import slash_commands

class Aichatbot(slash_commands.SlashCommand):
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
        return "Use aichatbot api to generate a response."

    @property
    def enabled_guilds(self):
        return None

    async def callback(self, context:slash_commands.SlashCommandContext) -> None:
        if context.guild_id == None:
            await context.respond('Command only availible on a guild channel')
            return None
        url = "https://ai-chatbot.p.rapidapi.com/chat/free"
        sentence = context.options['message'].value
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
            self.requests_abstract,
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
            
    @staticmethod 
    def requests_abstract(url, headers, querystring):
        """abstract the requests call"""
        res = requests.request("GET", url, headers=headers, params=querystring)
        return res

def load(bot:Bot):
    bot.add_slash_command(Aichatbot)