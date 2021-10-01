"""A simple Telegram bot that sends random dog pictures.

This code declares a Telegram bot that will reply every message with
a random dog picture.

Every picture is fetched through the Dog API (https://dog.ceo/dog-api/).

@author Andrés Ignacio Torres <andresitorresm@gmail.com>
"""

import logging
import os
import random

import requests
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


class DogPicsBot:
    """
    A class to encapsulate all relevant methods of the Dog Pics
    Telegram bot.
    """

    telegram_group = 'group'
    telegram_supergroup = 'supergroup'

    def __init__(self):
        """
        Constructor of the class. Initializes certain instance variables
        and checks if everything's O.K. for the bot to work as expected.
        """

        # This environment variable should be set before using the bot
        self.token = os.environ.get('DPB_TG_TOKEN')
        self.api_url = 'https://dog.ceo/api/breeds/image/random'
        self.dog_emojis = [
            "🐶",
            "🐕",
            "🐩",
            "🌭",
            "🦮",
            "🦴",
            "🐾",
        ]

        # These will be checked against as substrings within each
        # message, so different variations are not required if their
        # radix is present (e.g. "pup" covers "puppy" and "pupper" too)
        self.dog_triggers = [
            "woof",
            "bark",
            "pup",
            "dog",
            "perr",
            "lomito",
        ] + self.dog_emojis

        self.api_fox_url = 'https://randomfox.ca/floof/'

        # Just like dog triggers, these will be checked against
        # as substrings, variations are not required
        self.fox_triggers = [
            "🦊",
            "zorr",
            "fox",
            "vixen",
            "fennec",
        ]

        # Same as earlier triggers, but for sad messages
        self.sad_triggers = [
            "😔",
            "😢",
            "😭",
            "😓",
            "sad",
            "not good",
            "unhappy",
            "depressed",
            "miserable",
            "down",
            "downhearted",
            'triste',
        ]

        self.fetch_breeds()
        self.api_breeds_url = 'https://dog.ceo/api/breed/{0}/images/random'

        # Stops runtime if the token has not been set
        if self.token is None:
            raise RuntimeError(
                "FATAL: No token was found. " + \
                "You might need to specify one or more environment variables.")

        # Configures logging in debug level to check for errors
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)

    def fetch_breeds(self):
        """
        Fetches and stores in memory the list of searchable breeds.
        """

        response = requests.get(url="https://dog.ceo/api/breeds/list/all")
        response_body = response.json()
        breeds = list(response_body['message'])
        self.breeds = breeds

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

        # Declares and adds a handler for text messages that will reply with
        # a dog pic if either the message comes from a personal chat
        # or includes a trigger word
        text_handler = MessageHandler(Filters.text, self.handle_text_messages)
        self.dispatcher.add_handler(text_handler)

        # Declares and adds a handler for stickers that will reply with
        # a dog pic if the sticker is dog-related
        sticker_handler = MessageHandler(Filters.sticker, self.handle_stickers)
        self.dispatcher.add_handler(sticker_handler)

        # Fires up the polling thread. We're live!
        self.updater.start_polling()

    def get_dog_sound(self):
        """
        Randomly return a phrase similar to that of barking.
        """

        SOUNDS = [
            "Woof woof!",
            "Bark!",
            "Awoooo!",
            "Awroooo!",
            "Bark bark!",
        ]

        i = random.randint(0, len(SOUNDS) - 1)
        return SOUNDS[i]

    def show_help(self, update, context):
        """
        Sends the user a brief message explaining how to use the bot.
        """

        HELP_MSG = f"{self.get_dog_sound()} " + \
                   "If you want a dog picture, send me a message " + \
                   "or use the /dog command."
        context.bot.send_message(chat_id=update.message.chat_id, text=HELP_MSG)

    def handle_text_messages(self, update, context):
        """
        Checks if a message comes from a group. If that is not the case,
        or if the message includes a trigger word, replies with a dog picture.
        """
        words = set(update.message.text.lower().split())
        logging.debug(f'Received message: {update.message.text}')
        logging.debug(f'Splitted words: {", ".join(words)}')

        # Possibility: received message mentions a specific breed
        breed = None
        for b in self.breeds:
            if b in words:
                breed = b
                break
        mentions_a_breed = breed is not None

        # Easter Egg Possibility: has a fox emoji
        has_fox_emoji = any([x in words for x in self.fox_triggers])

        # Possibility: received a sad message
        is_sad_message = any([x in words for x in self.sad_triggers])

        # Possibility: received message mentions dogs
        should_trigger_picture = False
        for dog_trigger in self.dog_triggers:
            for word in words:
                if word.startswith(dog_trigger):
                    should_trigger_picture = True
                    break

        # Possibility: it's a personal chat message
        is_personal_chat = update.message.chat.type not in [self.telegram_group, self.telegram_supergroup]

        if has_fox_emoji:
            self.send_fox_picture(update, context)
        elif is_sad_message:
            self.send_dog_picture(update, context, breed, "Don't be sad, here is a cute dog!")
        elif any([should_trigger_picture, is_personal_chat, mentions_a_breed]):
            self.send_dog_picture(update, context, breed)

    def handle_stickers(self, update, context):
        """
        Checks if a given sticker is dog-related, and replies with a dog
        picture if that's the case.
        """

        has_sticker = update.message.sticker is not None
        has_emoji_sticker = has_sticker and update.message.sticker.emoji is not None
        has_dog_sticker = has_emoji_sticker and any([e in update.message.sticker.emoji for e in self.dog_emojis])

        if has_dog_sticker:
            self.send_dog_picture(update, context)

    def send_dog_picture(self, update, context, breed=None, caption=None):
        """
        Retrieves a random dog pic URL from the Dog API and sends the
        given dog picture as a photo message on Telegram.
        """

        if breed is not None:
            url = self.api_breeds_url.format(breed)
        else:
            url = self.api_url

        # Fetches a dog picture URL from the Dog API
        response = requests.get(url=url)
        response_body = response.json()
        image_url = response_body['message']

        if caption is not None:
            context.bot.send_photo(
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id,
                photo=image_url,
                caption=caption
            )
        else:
            # Sends the picture
            context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=image_url,
                caption=self.get_dog_sound()
            )


    def send_fox_picture(self, update, context):
        """
        Retrieves a random fox pic URL from the Fox API and sends the
        given fox picture as a photo message on Telegram.

        This is an easter egg!
        # TODO: Use only one "send_picture" method for both types
        """

        # Fetches a dog picture URL from the Dog API
        response = requests.get(url=self.api_fox_url)
        response_body = response.json()
        image_url = response_body['image']

        # Sends the picture
        context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=image_url,
            caption="Yip yip!"
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
