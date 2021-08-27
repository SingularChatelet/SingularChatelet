import os
import requests

import asyncio
from concurrent.futures import ThreadPoolExecutor

from discord.ext import commands

class Bot_AiChatbot(commands.Cog):
    def __init__(self, bot:commands.Bot):
        """Cogs related to AiChatbot api (on rapideapi)"""
        self.bot = bot
        print("Bot_AiChatbot init ready")
    
    @commands.command(aliases=["ss"])
    async def simsimi(self, ctx:commands.Context, *, sentence):
        """Use aichatbot api to generate a response."""
        async with ctx.typing():
            url = "https://ai-chatbot.p.rapidapi.com/chat/free"
            querystring = {"message":sentence, "uid":str(ctx.author.id)}
            key = os.environ.get('RAPID_API_KEY', None)
            if key == None:
                print('please provide a rapidapi key and subscribe to simsimi api')
                await ctx.send('Could not execute this command')
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
                await ctx.send('coul not execute this command')
                return None
            msg = resp.get('response', None)
            if msg == None:
                print(result.text)
                await ctx.send('Coul not execute this command')
                return None
            await self.bot.chatbot_send.send(ctx, msg)


    @staticmethod 
    def requests_abstract(url, headers, querystring):
        """abstract the requests call"""
        res = requests.request("GET", url, headers=headers, params=querystring)
        return res

def setup(bot:commands.Bot):
    bot.add_cog(Bot_AiChatbot(bot))