import discord
from discord.ext import commands

class On_Event(commands.Cog):
    def __init__(self, bot:commands.Bot):
        """When some discord bot event trigger."""
        self.bot = bot
        print('On_Event init ready!')

    @commands.Cog.listener()
    async def on_ready(self):
        """Bot connected to discord."""
        print('DISCORD BOT ready')
        status = discord.Status.online
        activity = discord.Game('speak with human | .help')
        await self.bot.change_presence(status=status, activity=activity)

    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error):
        """When an command error trigger."""
        if isinstance(error, commands.errors.CommandNotFound):
            if ctx.message.content.startswith('..'):
                return None
            await ctx.send("this command don't exists :eyes:")
            return None
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
            return None
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send_help(ctx.command)
            return None
        if isinstance(error, commands.errors.TooManyArguments):
            await ctx.send_help(ctx.command)
            return None
        await ctx.send(str(error))

def setup(bot:commands.Bot):
    bot.add_cog(On_Event(bot))