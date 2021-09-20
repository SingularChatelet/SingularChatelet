import hikari
from lightbulb import Bot
from lightbulb import slash_commands

class Help(slash_commands.SlashCommand):
    description="Help for a command or give list of commands"
    # Options:
    command : str = slash_commands.Option(
        description="Get Help for this command.",
        required=False
    )

    async def callback(self, context: slash_commands.SlashCommandContext) -> None:
        command = context.options.get('command')
        if command == None:
            all_commands = [x.name for x in context.bot.slash_commands]
            await context.respond(f"All commands : {', '.join(all_commands)}")
            return None
        command = context.bot.get_slash_command(command.name)
        if command == None:
            all_commands = [x.name for x in context.bot.slash_commands]
            await context.respond(
                f"This command dont exists\nAll commands : {', '.join(all_commands)}"
            )
            return None
        await context.respond(
            f'command name : {command.name}\ndescription : {command.description}'
        )

def load(bot:Bot):
    bot.add_slash_command(Help)