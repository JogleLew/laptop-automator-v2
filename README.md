# Laptop Automator V2
A Telegram bot for PCBeta to collect hackintosh laptop infomation

## Features

1. Grab information from PCBeta and filter
1. Easy to pick out
1. Write to local JSON file
1. Update to PCBeta by one click

## How to use

Require [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

Fill in the `BOT_TOKEN` in main.py

use `python main.py` to run the bot

When the bot is running, you can see all the instructions by sending `/help` to the bot.  

## Configuraion

the folder `config` should be placed in the same folder as the file `main.py`.

`fid.txt` used to store the fid, for macOS Sierra, it is 557.

`session.txt` used to store the session to access the threads list. A correct session is needed, or you will get nothing. You may need tools like Wireshark or Charles to help you get the session.

`threads.txt` used to store the threads to write. Every line of this file is `fid,tid,pid,page` illustrating a "floor" of forum. You should be the author of the "floor" due to the permission.

`value.txt` used to store the regex and the weight for the filter. Every line of this file is `regex=weight`.

`data.txt` is a local stoage of laptop infomation, using the JSON format.
