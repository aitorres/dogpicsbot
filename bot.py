"""A simple Telegram bot that sends random dog pictures.

This code declares a Telegram bot that will reply every message with
a random dog picture.

Every picture is fetched through the Dog API (https://dog.ceo/dog-api/).

@author Andrés Ignacio Torres <andresitorresm@gmail.com>
"""

import logging
import os

import requests
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


class DogPicsBot:
    """
    A class to encapsulate all relevant methods of the Dog Pics
    Telegram bot.
    """

    def __init__(self):
        """
        Constructor of the class. Initializes certain instance variables
        and checks if everything's O.K. for the bot to work as expected.
        """

        # This environment variable should be set before using the bot
        self.token = os.environ.get('DPB_TG_TOKEN')
        self.api_url = 'https://dog.ceo/api/breeds/image/random'

        # Stops runtime if the token has not been set
        if self.token is None:
            raise RuntimeError(
                "FATAL: No token was found. " + \
                "You might need to specify one or more environment variables.")

        # Configures logging in debug level to check for errors
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)

    def run_bot(self):
        """
        Sets up the required bot handlers and starts the polling
        thread in order to successfully reply to messages.
        """

        # Instantiates the bot updater
        self.updater = Updater(self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        # Declares and adds handlers for commands that shows help info
        start_handler = CommandHandler('start', self.show_help)
        help_handler = CommandHandler('help', self.show_help)
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(help_handler)

        # Declares and adds a handler to send a dog picture on demand
        dog_handler = CommandHandler('dog', self.send_dog_picture)
        self.dispatcher.add_handler(dog_handler)

        # Declares and adds a handler that will reply with a dog pic, if
        # the message received does not come from a group
        echo_handler = MessageHandler(Filters.text, self.echo_direct_messages)
        self.dispatcher.add_handler(echo_handler)

        # Fires up the polling thread. We're live!
        self.updater.start_polling()

    def show_help(self, update, context):
        """
        Sends the user a brief message explaining how to use the bot.
        """

        HELP_MSG = "Woof woof! " + \
                   "If you want a dog picture, send me a message " + \
                   "use the \\dog command."
        context.bot.send_message(chat_id=update.message.chat_id, text=HELP_MSG)

    def echo_direct_messages(self, update, context):
        """
        Checks if a message comes from a group. If that is not the case,
        replies with a dog picture.
        """

        if update.message.chat.type == 'group':
            return

        self.send_dog_picture(update, context)

    def send_dog_picture(self, update, context):
        """
        Retrieves a random dog pic URL from the Dog API and sends the
        given dog picture as a photo message on Telegram.
        """

        # Fetches a dog picture URL from the Dog API
        response = requests.get(url=self.api_url)
        response_body = response.json()
        image_url = response_body['message']

        # Sends the picture
        context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=image_url,
            caption="Woof woof!"
        )

def main():
    """
    Entry point of the script. If run directly, instantiates the
    DogPicsBot class and fires it up!
    """

    dog_pics_bot = DogPicsBot()
    dog_pics_bot.run_bot()

# If the script is run directly, fires the main procedure
if __name__ == "__main__":
    main()
