import datetime

from discord.ext import commands
from discord.ext import tasks

class ClearTask(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.clear_conversations.start()
        print("Tasks_ClearConversation init ready!")

    @tasks.loop(minutes=5)
    async def clear_conversations(self):
        await self.bot.wait_until_ready()
        to_remove = []
        for guild, conversations in self.bot.conversations.items():
            for user, conversation in conversations.items():
                time_marge = datetime.datetime.now() - datetime.timedelta(minutes=5)
                if conversation['time'] < time_marge:
                    to_remove.append((guild, user))
        for guild, user in to_remove:
            del self.bot.conversations[guild][user]

    @commands.guild_only()
    @commands.command()
    async def clear_my_history(self, ctx:commands.Context):
        """Clear message history of the user for .pt"""
        guild = str(ctx.guild.id)
        user = str(ctx.author.id)
        if guild not in self.bot.conversations:
            await ctx.send('no conversation history for now')
            return None
        if user not in self.bot.conversations[guild]:
            await ctx.send('no conversation history for now')
            return None
        del self.bot.conversations[guild][user]
        await ctx.send('Conversation history delete!')

def setup(bot:commands.Bot):
    bot.add_cog(ClearTask(bot))