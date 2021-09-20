import hikari
from lightbulb import Bot
from lightbulb import slash_commands

class Settings(slash_commands.SlashCommandGroup):
    description="Settings for all chatbot commands"

@Settings.subcommand()
class Set_Bot(slash_commands.SlashSubCommand):
    description="Create a custom webhook with name and avatar url. The ChatBot will speek with it."
    # Options:
    bot_name : str = slash_commands.Option(
        description="Pseudo for your custom chatbot.",
        required=True
    )
    avatar_url : str = slash_commands.Option(
        description="Avatar url for your custom chatbot.",
        required=True
    )

    async def callback(self, context: slash_commands.SlashCommandContext) -> None:
        if context.guild_id == None:
            await context.respond('Command only availible on guild channel')
            return None
        if not await context.bot._chatbot_send.has_manage_webhook_permission(context):
            await context.respond('The bot has no permissions to create a webhook.')
            return None
        name = context.options['bot_name'].value
        avatar_url = context.options['avatar_url'].value
        await context.bot._chatbot_send.create_webhook_for(context, name, avatar_url)

@Settings.subcommand()
class Remove_Bot(slash_commands.SlashSubCommand):
    description="Remove your custom webhook in this channel"

    async def callback(self, context:slash_commands.SlashCommandContext) -> None:
        if context.guild_id == None:
            await context.respond('Command only availible on guild channel')
            return None
        if not await context.bot._chatbot_send.has_manage_webhook_permission(context):
            await context.respond('The bot has no permissions to delete a webhook.')
            return None
        if not await context.bot._chatbot_send.is_webhook_name_exists(context.author.id, context.channel_id):
            await context.respond('This webhook name don\'t exists')
            return None
        await context.bot._chatbot_send.delete_webhook_from_db(context.author.id, context.channel_id)
        await context.respond('Custom webhook has been removed')

def load(bot:Bot):
    bot.add_slash_command(Settings)