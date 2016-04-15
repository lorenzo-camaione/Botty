#!/usr/bin/env python
# https://pypi.python.org/pypi/python-telegram-bot#telegram-api-supporthttps://pypi.python.org/pypi/python-telegram-bot#telegram-api-support
# https://pythonhosted.org/transmissionrpc/
import json
import logging
from six import wraps
import transmissionrpc
from telegram.ext import Updater


settings = json.loads(open('settings.json').read())
API_KEY = settings['api_key']
USERS_WHITE_LIST = settings['users'].values()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Setup a logger
logger = logging.getLogger(__name__)

# Setup BitTorrent client
torrent_client = transmissionrpc.Client('localhost', port=9091)


def login(function):
    @wraps(function)
    def wrapper(bot, update):
        if update.message.to_dict()['from']['id'] in USERS_WHITE_LIST:
            return function(bot, update)
        else:
            return bot.sendMessage(
                update.message.chat_id,
                text="Ask <Botty's owner> to add your user_id to  user_id white list"
            )
    return wrapper


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start_command(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help_command(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo_command(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


@login
def download_command(bot, update):
    arguments = update.message.text.split(' ')
    try:
        torrent_client.add_torrent(arguments[1])
    except Exception as e:
        text = str(e)
    else:
        text = 'Success'
    bot.sendMessage(update.message.chat_id, text=text)


@login
def status_command(bot, update):
    arguments = update.message.text.split(' ')
    try:
        torrent = torrent_client.get_torrents()[int(arguments[1])]
    except IndexError:
        text = 'No such torrent'
    except Exception as e:
        text = str(e)
    else:
        text = 'Name: %s\nProgress: %s \nETA: %s\nStatus: %s \n'.format(
                torrent.name, int(torrent.progress), torrent.format_eta(), torrent.status
        )
    bot.sendMessage(update.message.chat_id, text=text)


def error_handler(bot, update, error):
    logger.warn("Update '%s' caused error '%s'" % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=API_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.addTelegramCommandHandler('start', start_command)
    dispatcher.addTelegramCommandHandler('help', help_command)
    dispatcher.addTelegramCommandHandler('download', download_command)
    dispatcher.addTelegramCommandHandler('status', status_command)

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.addTelegramMessageHandler(echo_command)

    # log all errors
    dispatcher.addErrorHandler(error_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
