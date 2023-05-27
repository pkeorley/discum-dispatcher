import inspect
from typing import Union, List

from client import Client
from modules.utils import parse_args


__version__ = "1.0.0"
__author__ = "pkeorley"


class Dispatcher:
    def __init__(self,
                 bot: Client,
                 command_prefix:
                 Union[List[str], str] = "!"
                 ):
        self.bot = bot
        self.command_prefix = [command_prefix] if isinstance(command_prefix, str) else command_prefix
        self.commands = {}

    def add_command(self, name: str = None):
        def decorator(func):
            signature = inspect.signature(func)
            self.commands[name or func.__name__] = {
                "function": func,
                "parameters": parse_args(signature.parameters),
            }
            return func
        return decorator

    def get_commands(self):
        return self.commands

    def process_commands(self, response):
        message = response.parsed.auto()
        for command_name, other in self.get_commands().items():
            if message.get("content").startswith(tuple([prefix + command_name for prefix in self.command_prefix])):
                other["function"](response)

    def enabled_help(self, enabled: bool = True):
        if enabled:
            @self.add_command(name="help")
            def help_command(response):
                message = response.parsed.auto()
                channel_id = message["channel_id"]
                command_prefix = self.command_prefix[0] if len(self.command_prefix) == 1\
                    else "({})".format("|".join(self.command_prefix))
                self.bot.sendMessage(
                    channel_id,
                    "```py\nHi. Here you can see the list of example-bot commands you can use, for more information "
                    "go here:"
                    "https://github.com/pkeorley/discum-dispatcher\n\n{1}\n\nDispatcher Module version: {0}```".format(
                        __version__,
                        "\n".join(
                            f"{command_prefix}{command_name}"
                            for command_name, other in self.get_commands().items()
                        )
                    )
                )
