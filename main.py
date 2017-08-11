#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import util
import crawler
import json
import write

# Initial telegram python bot
BOT_TOKEN = 'fill in your bot token here'
updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        level=logging.INFO
)

# Get global variables
fid = 0
cookies = {}
threads = []
regex = {}
data = {}
update_mode = False
update_progress = 0
update_list = []

def init():
    global fid
    global cookies
    global threads
    global regex
    global data
    fid = util.read_fid()
    cookies = util.read_cookies()
    threads = util.read_threads()
    regex = util.read_value()
    data = util.read_data()

init()

def reload_all(bot, update):
    logging.info('reload_all')
    init()
    update_mode = False
    update_progress = 0
    update_list = []
    bot.send_message(
			chat_id=update.message.chat_id,
			text="Config file and data file reloaded."
	)

def stat_all(bot, update):
    global data
    logging.info('stat')
    msg = ''
    msg = msg + 'Last Update Date: ' + data['lastUpdateTime'] + '\n'
    msg = msg + 'Last Update Thread ID: ' + data['lastUpdateThread'] + '\n'
    msg = msg + 'Brand Data: \n'
    keys = ['Acer', 'Asus', 'Dell', 'Hasee', 'HP', 'Lenovo', 'MSI', 'Samsung', 'Sony', 'Toshiba', 'Others']
    for key in keys:
        msg = msg + '    ' + key + ': ' + str(len(data['data'][key])) + ' items;\n'
    bot.send_message(
        chat_id=update.message.chat_id,
        text=msg
    )


def display_help(bot, update):
    logging.info('help')
    bot.send_message(
            chat_id=update.message.chat_id, 
            text="Laptop Automator is a bot that helps to fetch new threads from PCBeta , record Hackintosh laptops installation threads and publish to PCBeta. Instructions: \n/help : Display help information\n/update : Start update mode\n/next : Display next thread information\n/add `OEM` : Add thread to certain OEM in local data\n/insert `OEM` `tid` : Insert one thread to certain OEM in local data(not in update mode)\n/write : Write local data to PCBeta\n/reload : Reload config file and data file\n/stat : Show local statistic information"
    )

def do_update(bot, update):
    global fid
    global cookies
    global data
    global update_mode
    global update_progress
    global update_list
    logging.info('update')
    if update_mode:
        bot.send_message(
                chat_id=update.message.chat_id,
                text="Already in update mode, use /next to show next thread, or use /add `OEM` to add to certain OEM data."
        )
        return
    update_mode = True
    bot.send_message(
            chat_id=update.message.chat_id,
            text="Update Mode - On\nPreparing data..."
            )
    result = crawler.crawl(fid, cookies, data['lastUpdateTime'], data['lastUpdateThread'])
    update_progress = 0
    update_list = util.filter(result, regex)
    next_thread(bot, update)

def next_thread(bot, update):
    global update_mode
    global update_progress
    global update_list
    global data
    logging.info('next')
    if not update_mode:
        bot.send_message(
                chat_id=update.message.chat_id,
                text="Not in update mode, use /update to start update."
        )
        return
    if update_progress < len(update_list):
        item = update_list[update_progress]
        bot.send_message(
                chat_id=update.message.chat_id,
                text=str(update_progress+1) + '/' + str(len(update_list)) + ':\n' + item['title'] + '\nhttp://bbs.pcbeta.com/forum.php?mod=viewthread&tid=' + item['tid']
        )
        update_progress = update_progress + 1
    else:
        bot.send_message(
                chat_id=update.message.chat_id,
                text="Update Mode - Off"
        )
        data['lastUpdateTime'] = update_list[-1]['createTime']
        data['lastUpdateThread'] = update_list[-1]['tid']
        update_mode = False
        update_progress = 0
        update_list = []
        util.write_data(data)

def add_thread(bot, update, args):
    global data
    global update_mode
    global update_progress
    global update_list
    logging.info('add')
    if not update_mode:
        bot.send_message(
                chat_id=update.message.chat_id,
                text="Not in update mode, use /update to start update."
        )
        return
    if len(args) == 1 and args[0] in data['data']:
        item = update_list[update_progress - 1]
        data['data'][args[0]].append(item)
        bot.send_message(
                chat_id=update.message.chat_id,
                text="Added to group '" + args[0] + "'."
        )
    else:
        bot.send_message(
                chat_id=update.message.chat_id,
                text="Please input a correct group name."
        )

def write_pcbeta(bot, update):
    global data
    global threads
    global cookies
    logging.info('write')
    if update_mode:
        bot.send_message(
                chat_id=update.message.chat_id,
                text="Already in update mode, use /next to show next thread, or use /add `OEM` to add to certain OEM data."
        )
    bot.send_message(
            chat_id=update.message.chat_id,
            text="Writing to PCBeta...It'll take about 30 seconds."
    )
    write.writeData(data, threads, cookies)
    bot.send_message(
            chat_id=update.message.chat_id,
            text="All done."
    )

def insert_one(bot, update, args):
    global data
    logging.info('insert')
    if len(args) < 2 or len(args) > 2:
        display_help(bot, update)
        return
    oem = args[0]
    tid = args[1]
    obj = crawler.getThreadObj(cookies, tid)
    if oem not in data['data']:
        bot.send_message(
                chat_id=update.message.chat_id,
                text="Incorrect OEM name."
        )
        return
    index = -1
    if tid < data['data'][oem][0]['tid']:
        index = 0
        data['data'][oem].insert(index, obj)
    elif tid > data['data'][oem][-1]['tid']:
        index = len(data['data'][oem])
        data['data'][oem].append(obj)
    else:
        index = 1
        while True:
            if index == len(data['data'][oem]):
                break
            if tid > data['data'][oem][index - 1]['tid'] and tid < data['data'][oem][index]['tid']:
                data['data'][oem].insert(index, obj)
                break
            index = index + 1
    util.write_data(data)
    bot.send_message(
            chat_id=update.message.chat_id,
            text="Added to local data."
    )
        
def echo(bot, update):
    bot.send_message(
            chat_id=update.message.chat_id, 
            text="Sorry, I don't know what you mean."
    )
    print(update.message)

start_handler = CommandHandler('start', display_help)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', display_help)
dispatcher.add_handler(help_handler)

update_handler = CommandHandler('update', do_update)
dispatcher.add_handler(update_handler)

next_handler = CommandHandler('next', next_thread)
dispatcher.add_handler(next_handler)

add_handler = CommandHandler('add', add_thread, pass_args=True)
dispatcher.add_handler(add_handler)

write_handler = CommandHandler('write', write_pcbeta)
dispatcher.add_handler(write_handler)

reload_handler = CommandHandler('reload', reload_all)
dispatcher.add_handler(reload_handler)

stat_handler = CommandHandler('stat', stat_all)
dispatcher.add_handler(stat_handler)

insert_handler = CommandHandler('insert', insert_one, pass_args=True)
dispatcher.add_handler(insert_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()

print('bot started.')
