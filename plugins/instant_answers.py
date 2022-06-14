import requests
from urllib import parse

import asyncio
from concurrent.futures import ThreadPoolExecutor

import hikari
from hikari import embeds
from pyclass.abstract_bot_app import AbstractBotApp as Bot
import lightbulb

plugin = lightbulb.Plugin("InstantAnswer")

@plugin.command
@lightbulb.option("question", "Question for DuckDuckGo", required=True)
@lightbulb.command("ddg", "Get an Instant Response from duckduckgo.")
@lightbulb.implements(lightbulb.SlashCommand)
async def smth(context: lightbulb.Context) -> None:
    url = "https://api.duckduckgo.com/?q="
    search = parse.quote(context.options['question'])
    params = "&format=json&t=SingularChatelet"
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        ThreadPoolExecutor(),
        requests.get,
        url+search+params
    )
    content = result.json()
    emb = hikari.Embed(
        title='Instant Answer',
        description=f'search : {context.options["question"]}',
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
    res = await context.respond(emb)
    emb.set_footer(
        text='duckducgo instant answer',
        icon='https://duckduckgo.com/favicon.ico'
    )
    await res.edit(embed=emb)

def load(bot: Bot):
    bot.add_plugin(plugin)
