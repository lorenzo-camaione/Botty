#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.

"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""


# https://pypi.python.org/pypi/python-telegram-bot#telegram-api-supporthttps://pypi.python.org/pypi/python-telegram-bot#telegram-api-support
# https://pythonhosted.org/transmissionrpc/


from telegram.ext import Updater
import json
import logging
import transmissionrpc
import datetime

data = open('settings.json').read()
settings = json.loads(settings)
API_KEY = settings['API_KEY']
USERS_WHITE_LIST = settings['users'].values() #insert root USER_IDs

# Enable logging
logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.INFO)

logger = logging.getLogger(__name__)

tc = transmissionrpc.Client('localhost', port=9091)
#tc.get_torrents()

def _days_hours_minutes(td):
    return "days: %d hours: %d, minutes: %d"  % (td.days, td.seconds//3600, (td.seconds//60)%60)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start_command(bot, update):
	bot.sendMessage(update.message.chat_id, text='Hi!')


def help_command(bot, update):
	bot.sendMessage(update.message.chat_id, text='Help!')


def echo_command(bot, update):
	bot.sendMessage(update.message.chat_id, text=update.message.text)


def download_torrent_command(bot, update):
	if login(bot, update): 
		arguments = update.message.text.split(' ')
		text = 'Success'
		try:
			tc.add_torrent(arguments[1])
		except Exception, e:
			text = str(e)
		bot.sendMessage(update.message.chat_id, text=text)
		

def show_torrent_status_command(bot, update):
	if login(bot, update): 
		arguments = update.message.text.split(' ')
		try:
			torrent = tc.get_torrents()[int(arguments[1])]
		except IndexError:
			text = 'No such torrent'
		except Exception, e:
			text = str(e)
		else:
			text = "name: %s\nProgress: %s \nETA: %s\nStato: %s \n" % (torrent.name, int(torrent.progress * 100) / 100, torrent.format_eta(), torrent.status)
		bot.sendMessage(update.message.chat_id, text=text) 

def login(bot, update):
	if update.message.to_dict()['from']['id'] in USERS_WHITE_LIST:
		return True
	bot.sendMessage(update.message.chat_id, text='Ask <Botty\'s owner> to add your user_id to  user_id white list')
	return False
	

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
	# Create the EventHandler and pass it your bot's token.
	updater = Updater(API_KEY)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.addTelegramCommandHandler("start", start_command)
	dp.addTelegramCommandHandler("help", help_command)
	dp.addTelegramCommandHandler("download", download_torrent_command)
	dp.addTelegramCommandHandler("status", show_torrent_status_command)

	# on noncommand i.e message - echo the message on Telegram
	dp.addTelegramMessageHandler(echo_command)

	# log all errors
	dp.addErrorHandler(error)

	# Start the Bot
	updater.start_polling()
	print("I'm active")

	# Run the bot until the you presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

if __name__ == '__main__':
	main()
