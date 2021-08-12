import os

from discord.ext import commands

def check_is_alowed():
    def predicate(ctx:commands.Context):
        list_alowed = [606758395583922176]
        return ctx.author.id in list_alowed
    return commands.check(predicate)

class Developper(commands.Cog):
    def __init__(self, bot:commands.Bot):
        """Developper commands."""
        self.bot = bot
        print('Developper init ready!')

    @commands.command()
    @commands.check_any(commands.is_owner(), check_is_alowed())
    async def shutdown(self, _):
        """Close the bot."""
        await self.bot.close()

    @commands.command()
    @commands.check_any(commands.is_owner(), check_is_alowed())
    async def delete_conversations(self, ctx:commands.Context):
        """Delete all current conversations history. Mainly for ressource usage."""
        counter = len(self.bot.conversations.keys())
        self.bot.conversations = {}
        await ctx.send(f'delete {counter} conversations')

    @commands.command()
    @commands.check_any(commands.is_owner(), check_is_alowed())
    async def re_init_transformers_data(self, ctx:commands.Context):
        """If the data is corumpted by bias, re init the data."""
        for file in os.listdir('data/transformers'):
            if not file.endswith('.txt'):
                os.remove(f'data/transformers/{file}')
        try: self.bot.unload_extension(f'cogs.bot_transformers')
        except commands.ExtensionNotLoaded: pass
        try: self.bot.load_extension(f'cogs.bot_transformers')
        except Exception as e: await ctx.send(str(e))
        else: await ctx.send('Transformers Data Re Init')
        
def setup(bot:commands.Bot):
    bot.add_cog(Developper(bot))