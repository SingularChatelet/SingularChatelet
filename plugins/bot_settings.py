import hikari
from lightbulb import Bot
from lightbulb import slash_commands

class Settings(slash_commands.SlashCommandGroup):
    @property
    def description(self) -> str:
        return "Settings for all chatbot commands"

    @property
    def enabled_guilds(self):
        return None

@Settings.subcommand()
class Set_Bot(slash_commands.SlashSubCommand):
    @property
    def options(self):
        return [
            hikari.CommandOption(
                name="name",
                description="Pseudo for your custom chatbot.",
                type=hikari.OptionType.STRING,
                is_required=True
            ),
            hikari.CommandOption(
                name="avatar_url",
                description="Avatar url for your custom chatbot.",
                type=hikari.OptionType.STRING,
                is_required=True
            )
        ]

    @property
    def description(self) -> str:
        return "Create a custom webhook with name and avatar url. The ChatBot will speek with it."

    async def callback(self, context: slash_commands.SlashCommandContext) -> None:
        if context.guild_id == None:
            await context.respond('Command only availible on guild channel')
            return None
        if not await context.bot._chatbot_send.has_manage_webhook_permission(context):
            await context.respond('The bot has no permissions to create a webhook.')
            return None
        name = context.options['name'].value
        avatar_url = context.options['avatar_url'].value
        await context.bot._chatbot_send.create_webhook_for(context, name, avatar_url)

@Settings.subcommand()
class Remove_Bot(slash_commands.SlashSubCommand):
    @property
    def options(self):
        return []

    @property
    def description(self) -> str:
        return "Remove your custom webhook in this channel"

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