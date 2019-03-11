# [CostituzioneBot](https://telegram.me/CostituzioneBot)

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](./LICENSE) [![License: GPL v3](https://img.shields.io/badge/Dev-%20@hearot-blue.svg)](https://telegram.me/hearot)

A Telegram bot which allows you to retrieve articles of the **Italian constitution**.
You can get more information on [Wikipedia](https://en.wikipedia.org/wiki/Constitution_of_Italy).

To run the bot yourself, you will need:
- Python (tested with 3.7)
- The [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) module

## Setup
- Get a token from [@BotFather](http://telegram.me/BotFather).
- Activate the *Inline mode* using the `/setinline` command with [@BotFather](http://telegram.me/BotFather).
- Install the requirements (using `virtualenv` is recommended) using `pip install -r requirements.txt`
- Then, you can run the bot using `python bot.py -t BOT_TOKEN`.