import os
import datetime
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Transformers
try:
    import torch
    torch_availibe = True
except ModuleNotFoundError:
    torch_availibe = False

import asyncio
from concurrent.futures import ThreadPoolExecutor

from pyclass.abstract_bot_app import AbstractBotApp as Bot
import lightbulb

plugin = lightbulb.Plugin("Pytorch")

def wraper_tokenizer_encode(bot, text, return_tensors):
    return bot._transformers_tokenizer.encode(
        text + bot._transformers_tokenizer.eos_token,
        return_tensors=return_tensors
    )

def wraper_create_history_inputs(bot, inputs, guild_id, user_id):
    guild = str(guild_id)
    user = str(user_id)
    if guild not in bot._transformers_conversations:
        bot._transformers_conversations[guild] = {}
    if user not in bot._transformers_conversations[guild]:
        bot._transformers_conversations[guild][user] = {}
        bot._transformers_conversations[guild][user]['data'] = inputs
        bot._transformers_conversations[guild][user]['time'] = datetime.datetime.now()
    else:
        time_marge = datetime.datetime.now() - datetime.timedelta(minutes=5)
        if bot._transformers_conversations[guild][user]['time'] < time_marge:
            bot._transformers_conversations[guild][user] = {}
            bot._transformers_conversations[guild][user]['data'] = inputs
            bot._transformers_conversations[guild][user]['time'] = datetime.datetime.now()
        else:
            bot._transformers_conversations[guild][user]['data'] = torch.cat(
                [bot._transformers_conversations[guild][user]['data'], inputs],
                dim=-1
            )
        bot._transformers_conversations[guild][user]['time'] = datetime.datetime.now()
    return bot._transformers_conversations[guild][user]['data']

def wraper_model_generate(bot, inputs):
    return bot._transformers_model.generate(
        inputs,
        max_length=1000,
        do_sample=True,
        top_p=0.95,
        top_k=100,
        temperature=0.75,
        pad_token_id=bot._transformers_tokenizer.eos_token_id
    )

def wraper_tokenizer_decode(bot, outputs, inputs_history):
    return bot._transformers_tokenizer.decode(
        outputs[:,inputs_history.shape[-1]:][0],
        skip_special_tokens=True
    )

@plugin.command
@lightbulb.option("message", "the message", required=True)
@lightbulb.command("pytorch", "Uses microsoft/DialoGPT-large and pytorch to generate the response.")
@lightbulb.implements(lightbulb.SlashCommand)
async def smth(context: lightbulb.Context) -> None:
    if torch_availibe == False:
        return
    if context.guild_id == None:
        await context.respond('Command only availible on guild channel')
        return None
    loop = asyncio.get_event_loop()
    inputs = await loop.run_in_executor(
        ThreadPoolExecutor(),
        wraper_tokenizer_encode,
        context.bot,
        context.options['message'],
        'pt'
    )
    inputs_history = await loop.run_in_executor(
        ThreadPoolExecutor(),
        wraper_create_history_inputs,
        context.bot,
        inputs,
        context.guild_id,
        context.author.id
    )
    outputs = await loop.run_in_executor(
        ThreadPoolExecutor(),
        wraper_model_generate,
        context.bot,
        inputs_history
    )
    response = await loop.run_in_executor(
        ThreadPoolExecutor(),
        wraper_tokenizer_decode,
        context.bot,
        outputs,
        inputs_history
    )
    if len(str(response)) < 1:
        await context.respond('[system message] no reponse for that')
        return None
    await context.bot._chatbot_send.send(context, str(response), context.options['message'])

def load(bot:Bot):
    if bot._full_bot_transformers == False:
        return None
    bot.add_plugin(plugin)
