from discord.ext import commands

import asyncio
from concurrent.futures import ThreadPoolExecutor

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Transformers
import torch
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

class Bot_Transformers(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        # pre_trained possibility : microsoft/DialoGPT-large | microsoft/DialoGPT-medium | microsoft/DialoGPT-small
        self._tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium", cache_dir='./data/transformers/')
        self._model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium", cache_dir='./data/transformers/')
        self.conversation = {}
        print('Bot_Transformers init ready!')

    @commands.command(aliases=['pytorch'])
    async def pt(self, ctx:commands.Context, *, sentence):
        """Uses microsoft/DialoGPT-large and pytorch to generate the response."""
        async with ctx.typing():
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
            await ctx.send(str(response), reference=ctx.message.to_reference())

    def wraper_tokenizer_encode(self, text, return_tensors):
        return self._tokenizer.encode(
            text + self._tokenizer.eos_token,
            return_tensors=return_tensors
        )
    
    def wraper_create_history_inputs(self, inputs, guild_id, user_id):
        guild = str(guild_id)
        user = str(user_id)
        if guild not in self.conversation:
            self.conversation[guild] = {}
        if user not in self.conversation[guild]:
            self.conversation[guild][user] = inputs
        else:
            self.conversation[guild][user] = torch.cat(
                [self.conversation[guild][user], inputs],
                dim=-1
            )
        return self.conversation[guild][user]

    def wraper_model_generate(self, inputs):
        return self._model.generate(
            inputs,
            max_length=1000,
            do_sample=True,
            top_k=100,
            top_p=0.95,
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