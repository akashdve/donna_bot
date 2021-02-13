import logging
import os

from py_dotenv import read_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from bot_handlers import start, good_echo, button, empty_message, college_updates


if __name__ == '__main__':

    try:
        read_dotenv(".env")
    except Exception as e:
        print("Error while reading env file - {}".format(e))

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                         level=logging.INFO)


    updater = Updater(os.getenv("SECRET_TOKEN"))

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('collegeupdates', college_updates))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), good_echo))
    updater.dispatcher.add_handler(MessageHandler(Filters.status_update, empty_message))



    updater.start_polling()
    updater.idle()
