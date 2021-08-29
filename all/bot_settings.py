import aiohttp
from discord import Webhook

from discord.ext import commands

class Bot_Settings(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command()
    async def set_my_bot(self, ctx:commands.Context, avatar_url:str, *, name):
        """Create a custom webhook with name and avatar url. The ChatBot will speek with it."""
        if not await self.bot.chatbot_send.has_manage_webhook_permission(ctx):
            await ctx.send('The bot has no permissions to create a webhook.')
            return None
        urls = await self.bot.chatbot_send.create_webhook_for(ctx, name, avatar_url)
        if urls == None:
            return None
        async with aiohttp.ClientSession() as session:
            web_hook = Webhook.from_url(urls[0], session=session)
            await web_hook.send('New webhook has been created', avatar_url=urls[1])

    @commands.command()
    async def remove_my_bot(self, ctx:commands.Context, *, name):
        """Remove your custom webhook named 'name'"""
        if not await self.bot.chatbot_send.has_manage_webhook_permission(ctx):
            await ctx.send('The bot has no permissions to delete a webhook.')
            return None
        if not await self.bot.chatbot_send.is_webhook_name_exists(ctx.author.id, name):
            await ctx.send('This webhook name don\'t exists')
            return None
        await self.bot.chatbot_send.delete_webhook_from_db(ctx.author.id, name)
        await ctx.send('Custom webhook has been removed')
        

def setup(bot:commands.Bot):
    bot.add_cog(Bot_Settings(bot))