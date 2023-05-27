## Python Discord S.C.U.M (discum) prefix-commands manager
- The utility is designed to add prefix commands to your bot without writing crutches
- It will help you easily create and manage commands
### Requirements
```bash
pip install -r requirements.txt
```
# Mehtods
```python
from client import Client
import dispatcher

print(dispatcher.__version__)  # Version
print(dispatcher.__author__)  # Author 

bot = Client(token=..., log=...)
dp = dispatcher.Dispatcher(bot)

@dp.add_command(name=...)
def name(response):
    ...

dp.get_commands()  # {commands} | dp.commands
dp.enabled_help(enabled=...)

print(dp.commands)  # {commands} | dp.get_commands()
print(dp.bot is bot) #  bot
print(dp.command_prefix)  # [prefixes]
```
### Examples

- An example of creating a bot with prefix commands

![Example of bot](https://i.imgur.com/kkeMZr1.png)

- Here is the code
```python
from dotenv import dotenv_values

from client import Client
from dispatcher import Dispatcher
from modules.utils import get_args


#  Creating a bot variable and put a bot token in it
values = dotenv_values("../venv/.env")
token = values["TOKEN"]

bot = Client(token=token, log=False)

#  Creating a command manager
dp = Dispatcher(bot, command_prefix=[".", "bot."])
dp.enabled_help(enabled=False)  # Disable help command, default enabled


#  Creates a prefix command that will repeat the text of the user
@dp.add_command(name="echo")
def echo(response):
    #  Initialize the variables that are important to us and that we will use further
    message = response.parsed.auto()
    args = get_args(response)
    channel_id = message["channel_id"]

    #  If the argument is empty, we send an error
    if not args:
        return bot.sendMessage(channel_id, "⛔ There is no text you would like to send, use like `{}echo`".format(
            dp.command_prefix[0]
        ))

    #  Send a message to the channel
    bot.sendMessage(channel_id, args)


@bot.gateway.command
def on_response(response):
    if response.event.ready_supplemental:
        print("Bot is ready to use!")

    if response.event.message:
        #  We load all our commands in order to process them
        dp.process_commands(response)


#  Let's launch our bot 😍
bot.gateway.run(auto_reconnect=True)
```
### A little bit about ../env/.env
```dotenv
TOKEN=bot_token
```