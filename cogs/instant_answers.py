import requests
from urllib import parse

import asyncio
from concurrent.futures import ThreadPoolExecutor

import discord
from discord.ext import commands

class InstantAnswer(commands.Cog):
    def __init__(self, bot:commands.Bot):
        """Get instant answer from some source."""
        self.bot = bot
        print('InstantAnswer init ready!')

    @commands.command(aliases=['ddg'])
    async def duckduckgo(self, ctx:commands.Context, *, answer):
        """Get an Instant Response from duckduckgo"""
        async with ctx.typing():
            url = "https://api.duckduckgo.com/?q="
            search = parse.quote(answer)
            params = "&format=json&t=SingularChatelet"
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                ThreadPoolExecutor(),
                requests.get,
                url+search+params
            )
            content = result.json()
            emb = discord.Embed(
                title=f'Instant Answer',
                description=f'search : {answer}',
                color=0x2ae53f
            )
            abstracttext = content.get('AbstractText', False)
            if bool(abstracttext):
                emb.add_field(
                    name='Topic Summary',
                    value=f'{abstracttext}\nSource : {content.get("AbstractURL", "no")}',
                    inline=False
                )
            answer = content.get('Answer', False)
            if bool(answer):
                emb.add_field(
                    name='Answer',
                    value=f'{answer}\nType : {content.get("AnswerType", "no")}',
                    inline=False
                )
            definition = content.get('Definition', False)
            if bool(definition):
                emb.add_field(
                    name='Definition',
                    value=f'{definition}\nSource : {content.get("DefinitionURL", "no")}',
                    inline=False
                )
            relatetopics = content.get('RelatedTopics', False)
            if bool(relatetopics):
                for topic in relatetopics:
                    value = topic.get('Text', False)
                    if bool(value):
                        emb.add_field(
                            name=topic.get('FirstURL', '...'),
                            value='click link to see more',
                            inline=True
                        )
            emb.set_footer(
                text='duckducgo instant answer',
                icon_url='https://duckduckgo.com/favicon.ico'
            )
            await ctx.send(embed=emb)

def setup(bot:commands.Bot):
    bot.add_cog(InstantAnswer(bot))