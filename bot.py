"""
A simple Telegram bot that sends random dog pictures.

This code declares a Telegram bot that will reply every message with
a random dog picture.

Every picture is fetched through the Dog API (https://dog.ceo/dog-api/).

@author Andrés Ignacio Torres <andresitorresm@gmail.com>
"""

import logging
import os
import random
from typing import List

import requests
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)


TELEGRAM_CHAT_TYPE_GROUP: str = "group"
TELEGRAM_CHAT_TYPE_SUPERGROUP: str = "supergroup"
TELEGRAM_GROUP_CHAT_TYPES: List[str] = [
    TELEGRAM_CHAT_TYPE_GROUP,
    TELEGRAM_CHAT_TYPE_SUPERGROUP,
]


DOG_SOUNDS: List[str] = [
    "Woof woof!",
    "Bark!",
    "Awoooo!",
    "Awroooo!",
    "Bark bark!",
    "Grrr!",
]

FOX_SOUNDS: List[str] = [
    "Grrr!",
    "Yip Yip!",
    "Ring-ding-ding-ding-dingeringeding!",
    "Wa-pa-pa-pa-pa-pa-pow!",
    "Hatee-hatee-hatee-ho!",
    "Joff-tchoff-tchoffo-tchoffo-tchoff!",
    "Jacha-chacha-chacha-chow!",
    "Fraka-kaka-kaka-kaka-kow!",
    "A-hee-ahee ha-hee!",
    "A-oo-oo-oo-ooo!",
]


DOGS_API_DOG_PICTURE_URL: str = "https://dog.ceo/api/breeds/image/random"
DOGS_API_SPECIFIC_BREED_DOG_PICTURE_URL: str = "https://dog.ceo/api/breed/{0}/images/random"
DOGS_API_BREED_LIST_URL: str = "https://dog.ceo/api/breeds/list/all"

RANDOMFOX_API_URL: str = "https://randomfox.ca/floof/"


# src: https://gist.github.com/bcnzer/2e1e392e355dc95b7f3da98a0b2ade9d
WOLF_PICTURES: List[str] = [
    "https://wolftracker9eee.blob.core.windows.net/wolfpictures-mock/wolf1.png",
    "https://wolftracker9eee.blob.core.windows.net/wolfpictures-mock/wolf2.png",
    "https://wolftracker9eee.blob.core.windows.net/wolfpictures-mock/wolf3.png",
    "https://wolftracker9eee.blob.core.windows.net/wolfpictures-mock/wolf4.png",
    "https://wolftracker9eee.blob.core.windows.net/wolfpictures-mock/wolf5.png",
    "https://wolftracker9eee.blob.core.windows.net/wolfpictures-mock/wolf6.png",
    "https://wolftracker9eee.blob.core.windows.net/wolfpictures-mock/wolf7.png",
    "https://wolftracker9eee.blob.core.windows.net/wolfpictures-mock/wolf8.png",
    "https://wolftracker9eee.blob.core.windows.net/wolfpictures-mock/wolf9.png",
]


def get_mentioned_breed(breeds, words):
    """
    Given a list of breeds and a list of words,
    checks if any breed appears within the list of words
    and returns the first successful case if so
    """

    for breed in breeds:
        # the breed might be directly mentioned
        # or it can be a substring (like)
        for word in words:
            if breed in word:
                return breed

    return None


class DogPicsBot:
    """
    A class to encapsulate all relevant methods of the Dog Pics
    Telegram bot.
    """

    REQUESTS_TIMEOUT = 10  # in seconds

    def __init__(self):
        """
        Constructor of the class. Initializes certain instance variables
        and checks if everything's O.K. for the bot to work as expected.
        """

        # Load environment variables
        load_dotenv()

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
            "pooch",
        ] + self.dog_emojis

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
        self.sad_spanish_triggers = [
            "triste",
            "afligido",
            "lloro",
            "deprimido",
            "tusa",
            "despech",  # despechado, despechada, despecho
        ]

        self.sad_triggers = [
            "😔",
            "😞",
            "😢",
            "😭",
            "😓",
            "😫",
            "💔",
            "sad",
            "not good",
            "unhappy",
            "depressed",
            "miserable",
            "down",
            "downhearted",
        ] + self.sad_spanish_triggers

        # And again, for wolves. I promise this is the last animal to be
        # introduced to the bot.
        self.wolf_triggers = [
            "🐺",
            "lobo",
            "wolf",
            "wolves",
            "howl",
        ]

        # This environment variable should be set before using the bot
        self.token = os.environ.get("DPB_TG_TOKEN")

        # Stops runtime if the token has not been set properly
        if not self.token:
            raise RuntimeError(
                "FATAL: No token was found. "
                "You might need to specify one or more environment variables."
            )

        # Fetches list of dog breeds from the Dogs API
        self.fetch_breeds()

        # Instantiates the bot application
        self.application = Application.builder().token(self.token).build()

    def fetch_breeds(self):
        """
        Fetches and stores in memory the list of searchable breeds.
        """

        response = requests.get(url=DOGS_API_BREED_LIST_URL, timeout=self.REQUESTS_TIMEOUT)
        response_body = response.json()
        self.breeds = list(response_body["message"])

    def run_bot(self):
        """
        Sets up the required bot handlers and starts the polling
        thread in order to successfully reply to messages.
        """

        # Declares and adds handlers for commands that shows help info
        start_handler = CommandHandler("start", self.show_help)
        help_handler = CommandHandler("help", self.show_help)
        self.application.add_handler(start_handler)
        self.application.add_handler(help_handler)

        # Declares and adds a handler to send a dog picture on demand
        dog_handler = CommandHandler("dog", self.send_dog_picture)
        self.application.add_handler(dog_handler)

        # Declares and adds a handler for text messages that will reply with
        # a dog pic if either the message comes from a personal chat
        # or includes a trigger word
        text_handler = MessageHandler(filters.TEXT, self.handle_text_messages)
        self.application.add_handler(text_handler)

        # Declares and adds a handler for stickers that will reply with
        # a dog pic if the sticker is dog-related
        sticker_handler = MessageHandler(filters.Sticker.ALL, self.handle_stickers)
        self.application.add_handler(sticker_handler)

        # Fires up the polling thread. We're live!
        self.application.run_polling()

    def get_random_dog_sound(self):
        """
        Randomly return a phrase similar to that of barking.
        """

        return random.choice(DOG_SOUNDS)

    def get_random_fox_sound(self):
        """
        Randomly return a phrase similar to that of Ding-ding-ding-ding.
        """

        return random.choice(FOX_SOUNDS)

    def get_random_wolf_picture(self):
        """
        Randomly return a link to a wolf's picture.
        """

        return random.choice(WOLF_PICTURES)

    async def show_help(self, update, context):
        """
        Sends the user a brief message explaining how to use the bot.
        """

        help_msg = (
            f"{self.get_random_dog_sound()} "
            + "If you want a dog picture, send me a message "
            + "or use the /dog command."
        )
        context.bot.send_message(chat_id=update.message.chat_id, text=help_msg)

    async def handle_text_messages(self, update, context):
        """
        Checks if a message comes from a group. If that is not the case,
        or if the message includes a trigger word, replies with a dog picture.
        """
        words = set(update.message.text.lower().split())
        logging.debug("Received message: %s", update.message.text)
        logging.debug("Splitted words: %s", ", ".join(words))

        # Possibility: received message mentions a specific breed
        mentioned_breed = get_mentioned_breed(self.breeds, words)
        mentions_a_breed = mentioned_breed is not None

        # Easter Egg Possibility: has a fox emoji or word
        has_fox_reference = any(
            any(word.startswith(fox_trigger) for word in words) for fox_trigger in self.fox_triggers
        )

        # Easter Egg Possibility: has a wolf emoji or word
        has_wolf_reference = any(
            any(word.startswith(wolf_trigger) for word in words)
            for wolf_trigger in self.wolf_triggers
        )

        # Possibility: received a sad message
        is_sad_message = any(
            any(word.startswith(sad_trigger) for word in words) for sad_trigger in self.sad_triggers
        )

        # Possibility: received message mentions dogs
        should_trigger_picture = any(
            any(word.startswith(dog_trigger) for word in words) for dog_trigger in self.dog_triggers
        )

        # Possibility: it's a personal chat message
        chat_type = update.message.chat.type
        is_personal_chat = chat_type not in TELEGRAM_GROUP_CHAT_TYPES

        if has_fox_reference:
            self.send_fox_picture(update, context)
        elif has_wolf_reference:
            self.send_wolf_picture(update, context)
        elif is_sad_message:
            sad_caption = "Don't be sad, have a cute dog!"
            await self.send_dog_picture(update, context, mentioned_breed, sad_caption)
        elif any([should_trigger_picture, is_personal_chat, mentions_a_breed]):
            await self.send_dog_picture(update, context, mentioned_breed)

    async def handle_stickers(self, update, context):
        """
        Checks if a given sticker is dog-related, and replies with a dog
        picture if that's the case.
        """

        has_sticker = update.message.sticker is not None
        has_emoji_sticker = has_sticker and update.message.sticker.emoji is not None
        has_dog_sticker = has_emoji_sticker and any(
            e in update.message.sticker.emoji for e in self.dog_emojis
        )

        if has_dog_sticker:
            await self.send_dog_picture(update, context)

    async def send_dog_picture(self, update, context, breed=None, caption=None):
        """
        Retrieves a random dog pic URL from the Dog API and sends the
        given dog picture as a photo message on Telegram.
        """

        url = (
            DOGS_API_DOG_PICTURE_URL
            if breed is None
            else DOGS_API_SPECIFIC_BREED_DOG_PICTURE_URL.format(breed)
        )

        # Fetches a dog picture URL from the Dog API
        response = requests.get(url=url, timeout=self.REQUESTS_TIMEOUT)
        response_body = response.json()
        image_url = response_body["message"]

        if caption is not None:
            self.send_picture(update, context, image_url, caption)
        else:
            self.send_picture(update, context, image_url, self.get_random_dog_sound())

    def send_fox_picture(self, update, context):
        """
        Retrieves a random fox pic URL from the Fox API and sends the
        given fox picture as a photo message on Telegram.
        """

        # Fetches a dog picture URL from the Dog API
        response = requests.get(url=RANDOMFOX_API_URL, timeout=self.REQUESTS_TIMEOUT)
        response_body = response.json()
        image_url = response_body["image"]

        self.send_picture(update, context, image_url, self.get_random_fox_sound())

    def send_wolf_picture(self, update, context):
        """
        Retrieves a random wolf pic URL from the static list and sends the
        given wolf picture as a photo message on Telegram.
        """

        image_url = self.get_random_wolf_picture()

        self.send_picture(update, context, image_url, "Howl!")

    def send_picture(self, update, context, image_url, caption):
        """
        Retrieves a pic URL from the provided API and sends the
        given picture as a photo reply message on Telegram.
        """
        # Sends the picture
        context.bot.send_photo(
            chat_id=update.message.chat_id,
            reply_to_message_id=update.message.message_id,
            photo=image_url,
            caption=caption,
        )


# If the script is run directly, fires the main procedure
if __name__ == "__main__":
    bot = DogPicsBot()
    bot.run_bot()
