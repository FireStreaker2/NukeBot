![NukeBot](https://socialify.git.ci/FireStreaker2/NukeBot/image?description=1&font=Raleway&forks=1&issues=1&language=1&name=1&owner=1&pulls=1&stargazers=1&theme=Dark)

# About
NukeBot was made to be quick and easy. A friend wanted it, and other nuke bots on GitHub didn't work out of the box. That's when NukeBot started being developed.

> [!WARNING]  
> This is for educational purposes only. I am not responsible for your actions.

# Usage
## Setup
To get started, follow the below steps.
```bash
$ git clone https://github.com/FireStreaker2/NukeBot.git
$ cd NukeBot
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ cp .env.example .env
$ python main.py
```

## Discord Configuration
> [!IMPORTANT]  
> The following is crucial information.   

Currently, the code in ``main.py`` requests for all of the intents. If you would like to only use the message content intent, you can change the code to the following. Otherwise, make sure to turn on all three intents in the [discord developer portal](https://discord.com/developers)
```python
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=config["Prefix"], intents=intents)
```

## Environment Variables
Currently, there are three environment variables which you can customize. 
| Variable | Description                |
|----------|----------------------------|
| Token    | The bot's token            |
| Status   | What the bot is "watching" |
| Prefix   | The bot's prefix           |

## Commands
NukeBot offers a variety of commands. They should be self-explanatory, but if you would like to know more you can look at the source code in ``main.py``.

> Note that this list uses ``.`` as the prefix, because that's the default prefix.

* ``.nuke <amount of channels> <amount of messages in each channel> <channel name> <message to put in every channel>``
* ``.dm <amount of messages to send> <message to send>``
* ``.banall``
* ``.deleteroles``
* ``.hoist <role name>``
* ``.deletechannels``
* ``.editserver <new name> [new logo url]``
* ``.help``

You can also see the ``help`` command for info inside discord.

# Contributing
If you would like to contribute, you can <a href="https://github.com/FireStreaker2/NukeBot/fork">fork the repo</a> and <a href="https://github.com/FireStreaker2/NukeBot/compare">make a PR</a>, or contact me via email @ ``suggestions@firestreaker2.gq``

# License
[MIT](https://github.com/FireStreaker2/NukeBot/blob/main/LICENSE)
