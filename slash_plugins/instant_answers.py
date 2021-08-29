import requests
from urllib import parse

import asyncio
from concurrent.futures import ThreadPoolExecutor

import hikari
from lightbulb import Bot
from lightbulb import slash_commands

class DuckCuckGo(slash_commands.SlashCommand):
    @property
    def options(self):
        return [
            hikari.CommandOption(
                name="question",
                description="Question for DuckDuckGo.",
                type=hikari.OptionType.STRING,
                is_required=True
            ),
        ]

    @property
    def description(self) -> str:
        return "Get an Instant Response from duckduckgo."

    @property
    def enabled_guilds(self):
        return None

    async def callback(self, context: slash_commands.SlashCommandContext) -> None:
        url = "https://api.duckduckgo.com/?q="
        search = parse.quote(context.options['question'].value)
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
            description=f'search : {context.options["question"].value}',
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
            icon=hikari.File('https://duckduckgo.com/favicon.ico')
        )
        await context.respond(embed=emb)

def load(bot:Bot):
    bot.add_slash_command(DuckCuckGo)