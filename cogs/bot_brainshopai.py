import os
import requests
import urllib.parse

import asyncio
from concurrent.futures import ThreadPoolExecutor

from discord.ext import commands
from urllib3 import response

class Bot_BrainShopAI(commands.Cog):
    def __init__(self, bot:commands.Bot):
        """Cogs related to brainshopAI api"""
        self.bot = bot
        print('Bot_BrainShopAi init ready')

    @commands.command(aliases=["bs"])
    async def brainshopai(self, ctx:commands.Context, *, sentence):
        """Use brainshopAI api to generate a response."""
        async with ctx.typing():
            msg = urllib.parse.quote_plus(sentence)
            bid = os.environ.get("BRAINSHOP_BID", None)
            if bid == None:
                print("You need to sign in to brainshop.ai and get your bid")
                await ctx.send('Could not execute this command')
                return None
            key = os.environ.get('BRAINSHOP_KEY', None)
            if key == None:
                print("You need to sign in to brainshop.ai and get your api key")
                await ctx.send('Could not execute this command')
                return None
            uid = ctx.author.id
            url = f"http://api.brainshop.ai/get?bid={bid}&key={key}&uid={uid}&msg={msg}"
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                ThreadPoolExecutor(),
                requests.get,
                url
            )
            resp = result.json()
            if 'cnt' not in resp.keys():
                await ctx.send(f'bad result : {resp}')
                return None
            await self.bot.chatbot_send.send(ctx, str(resp['cnt']))

def setup(bot:commands.Bot):
    bot.add_cog(Bot_BrainShopAI(bot))