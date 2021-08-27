from discord.ext import commands

class ClearTask(commands.Cog):
    def __init__(self, bot:commands.Bot):
        """Clear conversations history."""
        self.bot = bot
        print("Tasks_ClearConversation init ready!")

    @commands.guild_only()
    @commands.command()
    @commands.bot_has_permissions(manage_messages=True, read_message_history=True)
    async def clear_message_channel(self, ctx:commands.Context):
        """Clear your message and bot's message if it respond to you."""
        async with ctx.typing():
            counter = 0
            list_commands = ['.bs ', '.ac ', '.brainshopai', '.aichatbot']
            async for message in ctx.channel.history(oldest_first=False):
                if message.author.id == ctx.author.id:
                    for query in list_commands:
                        if message.content.startswith(query):
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