import datetime

from discord.ext import commands
from discord.ext import tasks

class ClearTask(commands.Cog):
    def __init__(self, bot:commands.Bot):
        """Clear conversations history."""
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
        """Clear message history of the user for .pt."""
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

    @commands.guild_only()
    @commands.command()
    @commands.bot_has_permissions(manage_messages=True, read_message_history=True)
    async def clear_message_channel(self, ctx:commands.Context):
        """Clear your message and bot's message if it respond to you."""
        async with ctx.typing():
            counter = 0
            async for message in ctx.channel.history(oldest_first=False):
                if message.author.id == ctx.author.id:
                    if message.content.startswith('.pt ') or message.content.startswith('.cb '):
                        await message.delete()
                        counter += 1
                if message.author.id == self.bot.user.id:
                    refer = message.reference
                    if refer != None:
                        if refer.resolved != None:
                            if refer.resolved.author.id == ctx.author.id:
                                await message.delete()
                                counter += 1
            await ctx.send(f'delete {counter} message(s)')

def setup(bot:commands.Bot):
    bot.add_cog(ClearTask(bot))