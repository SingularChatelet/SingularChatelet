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

def setup(bot:commands.Bot):
    bot.add_cog(ClearTask(bot))