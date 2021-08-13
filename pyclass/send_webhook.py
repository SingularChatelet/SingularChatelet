import aiosqlite
import sqlite3
import aiohttp

from discord import Webhook

from discord.ext.commands import Context

class SendWebhook():
    def __init__(self):
        self.db_path = 'data/db.sqlite3'
        with sqlite3.connect(self.db_path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS webhook_table (channel_id INTEGER, user_id INTEGER, Webhook_url TEXT, Avatar_url TEXT, Name TEXT)')
            db.commit()
        print('SendWebhook init ready!')

    async def send(self, ctx:Context, message:str):
        if not await self.has_manage_webhook_permission(ctx):
            await ctx.send(message, reference=ctx.message.to_reference())
            return None
        urls = await self.get_webhook_urls_for(ctx.channel.id ,ctx.author.id)
        if urls == None:
            await ctx.send(message, reference=ctx.message.to_reference())
            return None
        async with aiohttp.ClientSession() as session:
            web_hook = Webhook.from_url(urls[0], session=session)
            await web_hook.send(f'{message}\n||Reply to {ctx.author.name}||', avatar_url=urls[1])

    async def has_manage_webhook_permission(self, ctx:Context):
        """
        Check if bot has manage webhook permission.
        Code from discord.py.
        """
        guild = ctx.guild
        me = guild.me if guild is not None else ctx.bot.user
        permissions = ctx.channel.permissions_for(me)
        return getattr(permissions, 'manage_webhooks')

    async def create_webhook_for(self, ctx:Context, name:str, avatar_url:str):
        """Create a new webhook and return url and avatar url"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT * FROM webhook_table WHERE channel_id=? AND user_id=? AND Avatar_url=? AND Name=?', (ctx.channel.id, ctx.author.id, avatar_url, name)) as cursor:
                data = await cursor.fetchone()
        if data != None:
            await ctx.send('A webhook already exists (do `.help remove_my_bot`)')
            return None
        webhook = await ctx.channel.create_webhook(name=name)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('INSERT INTO webhook_table VaLUES (?,?,?,?,?)', (ctx.channel.id, ctx.author.id, webhook.url, avatar_url, name))
            await db.commit()
        return (webhook.url, avatar_url)

    async def get_webhook_urls_for(self, channel_id:int, user_id:int):
        """Return a webhook url and avatar url if user_id has set a webhook. Else None."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT Webhook_url, Avatar_url FROM webhook_table WHERE channel_id=? AND user_id=?', (channel_id, user_id)) as cursor:
                urls = await cursor.fetchone()
        return urls

    async def is_webhook_name_exists(self, user_id:int, name:str):
        """Check if the user have a webhook called name"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT Avatar_url FROM webhook_table WHERE user_id=? AND Name=?', (user_id, name)) as cursor:
                web_hook_name = await cursor.fetchone()
        return bool(web_hook_name)

    async def delete_webhook_from_db(self, user_id:int, name:str):
        """Delete data for a custom webhook"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('DELETE FROM webhook_table WHERE user_id=? AND Name=?', (user_id, name))
            await db.commit()
