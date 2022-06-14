import hikari
from pyclass.abstract_bot_app import AbstractBotApp as Bot
import lightbulb

plugin = lightbulb.Plugin("Settings")

@plugin.command
@lightbulb.command("bot", "Settings for all chatbot commands")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def parent(context: lightbulb.Context) -> None:
    await context.respond("Use the subcommands to set bot behaviour")

@parent.child
@lightbulb.option("bot_name", "Pseudo for your custom chatbot.", type=str, required=True)
@lightbulb.option("avatar_url", "Avatar url for your custom chatbot.", type=str, required=True)
@lightbulb.command("create_custom", "Create a custom webhook with name and avatar url. The ChatBot will speek with it.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def bot_func_bot(context: lightbulb.Context) -> None:
    if context.guild_id == None:
        await context.respond('Command only availible on guild channel')
        return None
    if not await context.bot._chatbot_send.has_manage_webhook_permission(context):
        await context.respond('The bot has no permissions to create a webhook.')
        return None
    name = context.options['bot_name']
    avatar_url = context.options['avatar_url']
    await context.bot._chatbot_send.create_webhook_for(context, name, avatar_url)

@parent.child
@lightbulb.command("remove_custom", "Create a custom webhook with name and avatar url. The ChatBot will speek with it.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def bot_func_rem(context: lightbulb.Context) -> None:
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
    bot.add_plugin(plugin)
