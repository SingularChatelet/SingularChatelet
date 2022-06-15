import hikari
from pyclass.abstract_bot_app import AbstractBotApp as Bot
import lightbulb

plugin = lightbulb.Plugin("Help")

@plugin.command
@lightbulb.option("command", "Get Help for this command.", required=False)
@lightbulb.command("help", "Help for a command or give list of commands")
@lightbulb.implements(lightbulb.SlashCommand)
async def smth(context: lightbulb.Context) -> None:
    command = context.options.get('command')
    if command == None:
        all_commands = [x for x in context.bot.slash_commands]
        await context.respond(f"All commands : {', '.join(all_commands)}")
        return None
    command = context.bot.get_slash_command(command.name)
    if command == None:
        all_commands = [x for x in context.bot.slash_commands]
        await context.respond(
            f"This command dont exists\nAll commands : {', '.join(all_commands)}"
        )
        return None
    await context.respond(
        f'command name : {command.name}\ndescription : {command.description}'
    )

def load(bot: Bot):
    bot.add_plugin(plugin)
