import sqlite3
import aiosqlite

from hikari import messages
import hikari
import lightbulb

class SendWebhook():
    def __init__(self):
        self.db_path = 'data/db.sqlite3'
        with sqlite3.connect(self.db_path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS webhook_table (channel_id INTEGER, user_id INTEGER, webhook_id TEXT, webhook_token TEXT)')
            db.commit()
        print('class::SendWebhook::init -> ready')

    async def send(self, ctx: lightbulb.Context, message:str, question:str = None) -> None:
        urls = await self.get_webhook_urls_for(ctx.channel_id, ctx.author.id)
        webhook_id = None
        try:
            webhook_id = int(urls[0])
        except Exception as _:
            pass
        if urls == None or webhook_id == None:
            bot_member = ctx.bot.cache.get_member(ctx.guild_id, ctx.bot.cache.get_me().id)
            if bot_member == None:
                return None
            message = f"{bot_member.username if bot_member == None else 'Bot'} >> {message}"
            if question != None:
                message = f"{ctx.author.username} >> {question}\n" + message
            await ctx.respond(message)
            return None
        if question != None:
            message = f"{ctx.author.username} >> {question}\n" + f"Reply >> {message}"
        await ctx.bot.rest.execute_webhook(
            token=urls[1],
            webhook=webhook_id,
            content=message
        )
        await ctx.respond('response sent', flags=messages.MessageFlag.EPHEMERAL)

    async def has_manage_webhook_permission(self, ctx: lightbulb.Context) -> bool:
        """Check if bot has manage webhook permission."""
        bot_member = ctx.bot.cache.get_member(ctx.guild_id, ctx.bot.cache.get_me().id)
        if bot_member == None:
            return False
        perms = hikari.Permissions.NONE
        for role in bot_member.get_roles():
            perms |= role.permissions
        return perms & hikari.Permissions.MANAGE_WEBHOOKS

    async def create_webhook_for(self, ctx: lightbulb.Context, name:str, avatar_url:str) -> None:
        """Create a new webhook and return url and avatar url"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT * FROM webhook_table WHERE channel_id=? AND user_id=?', (ctx.channel_id, ctx.author.id)) as cursor:
                data = await cursor.fetchone()
        if data != None:
            await ctx.respond('A webhook already exists (do `/help remove_my_bot`)')
            return None
        webhook = await ctx.bot.rest.create_webhook(
            channel=ctx.channel_id,
            name=name,
            avatar=avatar_url,
            reason=f'custom SingularChatelet response for {ctx.author.username}'
        )
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('INSERT INTO webhook_table VALUES (?,?,?,?)', (ctx.channel_id, str(ctx.author.id), str(webhook.id), webhook.token, ))
            await db.commit()
        await self.send(ctx, "webhook created")

    async def get_webhook_urls_for(self, channel_id:int, user_id:int) -> list:
        """Return a webhook url and avatar url if user_id has set a webhook. Else None."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT webhook_id, webhook_token FROM webhook_table WHERE channel_id=? AND user_id=?', (channel_id, user_id)) as cursor:
                urls = await cursor.fetchone()
        return urls

    async def is_webhook_name_exists(self, user_id:int, channel_id:int) -> bool:
        """Check if the user have a webhook called name"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT channel_id FROM webhook_table WHERE user_id=? AND channel_id=?', (user_id, channel_id)) as cursor:
                web_hook_name = await cursor.fetchone()
        return bool(web_hook_name)

    async def delete_webhook_from_db(self, user_id:int, channel_id:int) -> None:
        """Delete data for a custom webhook"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('DELETE FROM webhook_table WHERE user_id=? AND channel_id=?', (user_id, channel_id))
            await db.commit()
