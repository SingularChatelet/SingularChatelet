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

def setup(bot:commands.Bot):
    bot.add_cog(Developper(bot))
