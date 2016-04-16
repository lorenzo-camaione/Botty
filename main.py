#!/usr/bin/env python
# https://pypi.python.org/pypi/python-telegram-bot#telegram-api-supporthttps://pypi.python.org/pypi/python-telegram-bot#telegram-api-support
# https://pythonhosted.org/transmissionrpc/
import json
import logging
from six import wraps
import transmissionrpc
from telegram.ext import Updater

settings = json.loads(open('settings.json').read())
API_TOKEN = settings['api_token']
USERS_WHITE_LIST = settings['users'].values()

# Enable logging
logging.basicConfig(
    filename='log/app.log',
    format='[%(levelname)s] %(asctime)s - %(name)s:\n%(message)s',
    level=logging.INFO
)

# Setup logger
logger = logging.getLogger(__name__)

# Setup Transmission BitTorrent client
torrent_client = transmissionrpc.Client('localhost', port=9091)


def login(function: callable):
    @wraps(function)
    def wrapper(bot, update):
        if update.message.to_dict()['from']['id'] in USERS_WHITE_LIST:
            return function(bot, update)
        else:
            return bot.sendMessage(
                update.message.chat_id,
                text="Ask Botty's owner to add your user_id to the white list"
            )

    return wrapper


def parse_command_arguments(argc: int = 0):
    def decorator(function: callable):
        @wraps(function)
        def wrapper(bot, update):
            args = update.message.text.split(' ')[1:]
            if len(args) == argc:
                return function(bot, update, args[1:])
            else:
                return bot.sendMessage(
                    update.message.chat_id,
                    text='Invalid arguments: required {} argument{} but {} {} given'.format(
                        argc, 's' if argc > 1 else '', len(args), 'were' if len(args) > 1 else 'was'
                    )
                )

        return wrapper

    return decorator


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start_command(bot, update):
    bot.sendMessage(
        update.message.chat_id,
        text='Hi {}!\nWelcome back'.format(update.message.to_dict()['from']['username'])
    )


def help_command(bot, update):
    bot.sendMessage(
        update.message.chat_id,
        text='Help:\n\n'
             '/download <TORRENT-URL>\n'
             '/status <TORRENT-ID>'
    )


def echo_command(bot, update):
    bot.sendMessage(
        update.message.chat_id,
        text='Did you say: "{}"?'.format(update.message.text)
    )


@login
@parse_command_arguments(argc=1)
def download_command(bot, update, args):
    try:
        torrent_client.add_torrent(args[0])
    except Exception as e:
        logger.exception(e, exc_info=True)
        text = 'Something went wrong'
    else:
        text = 'Success'
    bot.sendMessage(update.message.chat_id, text=text)


@login
@parse_command_arguments(argc=1)
def status_command(bot, update, args):
    try:
        torrent = torrent_client.get_torrents()[int(args[0])]
    except IndexError:
        text = 'No such torrent'
    except Exception as e:
        logger.exception(e, exc_info=True)
        text = 'Something went wrong'
    else:
        text = 'Name: %s\nProgress: %s \nETA: %s\nStatus: %s \n'.format(
            torrent.name, int(torrent.progress), torrent.format_eta(), torrent.status
        )
    bot.sendMessage(update.message.chat_id, text=text)


def error_handler(_, update, error):
    logger.error("Update '{}' caused error '{}'".format(update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=API_TOKEN)

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
