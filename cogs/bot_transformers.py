import os
import datetime
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from discord.ext import commands

import asyncio
from concurrent.futures import ThreadPoolExecutor

# Transformers
import torch
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

class Bot_Transformers(commands.Cog):
    def __init__(self, bot:commands.Bot):
        """Cogs related to transformers lib."""
        self.bot = bot
        # pre_trained possibility : microsoft/DialoGPT-large | microsoft/DialoGPT-medium | microsoft/DialoGPT-small
        self._tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large", cache_dir='./data/transformers/')
        self._model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large", cache_dir='./data/transformers/')
        self.bot.conversations = {}
        print('Bot_Transformers init ready!')

    @commands.guild_only()
    @commands.command(aliases=['pytorch'])
    async def pt(self, ctx:commands.Context, *, sentence):
        """Uses microsoft/DialoGPT-large and pytorch to generate the response."""
        async with ctx.typing() as context_manager:
            loop = asyncio.get_event_loop()
            inputs = await loop.run_in_executor(
                ThreadPoolExecutor(),
                self.wraper_tokenizer_encode,
                sentence,
                'pt'
            )
            inputs_history = await loop.run_in_executor(
                ThreadPoolExecutor(),
                self.wraper_create_history_inputs,
                inputs,
                ctx.guild.id,
                ctx.author.id
            )
            outputs = await loop.run_in_executor(
                ThreadPoolExecutor(),
                self.wraper_model_generate,
                inputs_history
            )
            response = await loop.run_in_executor(
                ThreadPoolExecutor(),
                self.wraper_tokenizer_decode,
                outputs,
                inputs_history
            )
            if len(str(response)) < 1:
                await ctx.send(
                    '[system message] no reponse for that',
                    reference=ctx.message.to_reference()
                )
                return None
            await self.bot.chatbot_send.send(ctx, str(response))
            #await ctx.send('.', delete_after=0.1)

    def wraper_tokenizer_encode(self, text, return_tensors):
        return self._tokenizer.encode(
            text + self._tokenizer.eos_token,
            return_tensors=return_tensors
        )

    def wraper_create_history_inputs(self, inputs, guild_id, user_id):
        guild = str(guild_id)
        user = str(user_id)
        if guild not in self.bot.conversations:
            self.bot.conversations[guild] = {}
        if user not in self.bot.conversations[guild]:
            self.bot.conversations[guild][user] = {}
            self.bot.conversations[guild][user]['data'] = inputs
            self.bot.conversations[guild][user]['time'] = datetime.datetime.now()
        else:
            self.bot.conversations[guild][user]['data'] = torch.cat(
                [self.bot.conversations[guild][user]['data'], inputs],
                dim=-1
            )
            self.bot.conversations[guild][user]['time'] = datetime.datetime.now()
        return self.bot.conversations[guild][user]['data']

    def wraper_model_generate(self, inputs):
        return self._model.generate(
            inputs,
            max_length=1000,
            do_sample=True,
            top_p=0.95,
            top_k=100,
            temperature=0.75,
            pad_token_id=self._tokenizer.eos_token_id
        )

    def wraper_tokenizer_decode(self, outputs, inputs_history):
        return self._tokenizer.decode(
            outputs[:,inputs_history.shape[-1]:][0],
            skip_special_tokens=True
        )

def setup(bot:commands.Bot):
    bot.add_cog(Bot_Transformers(bot))