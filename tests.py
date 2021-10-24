"""
Unit tests for the functions and classes implemented for the DogPicsBot.

@author Andrés Ignacio Torres <andresitorresm@gmail.com>
"""

from dataclasses import dataclass, field
from random import randint
from typing import List, Optional, Tuple

import pytest
from bot import (
    DOGS_API_BREED_LIST_URL,
    DOGS_API_DOG_PICTURE_URL,
    RANDOMFOX_API_URL,
    TELEGRAM_CHAT_TYPE_GROUP,
    DOG_SOUNDS,
    DogPicsBot,
)


# Mocking Telegram's API
@dataclass
class MockDispatcher:
    """
    Mock class to bypass Telegram's dispatcher on tests.
    """

    handler_names: List[str] = field(default_factory=list)

    def add_handler(self, handler):
        """
        Fakes the process in which a new handler is added to a Telegram
        bot's dispatcher. Instead, stores the name of the new handler
        on an instance level for further checks on tests.
        """

        self.handler_names.append(handler.__name__)


@dataclass
class MockUpdater:
    """
    Mock class to bypass Telegram's updater on tests.
    """

    token: str
    use_context: bool = True
    dispatcher: MockDispatcher = MockDispatcher()

    def start_polling(self):
        """
        Fakes the call to Telegram's updater's start_polling, but in reality
        does nothing.
        """
        return


@dataclass
class MockChat:
    """
    Mocks the information contained in Telegram's Chat class for tests.
    """

    type: str


@dataclass
class MockSticker:
    """
    Mocks the information contained in Telegram's Sticker class for tests.
    """

    emoji: Optional[str] = None


@dataclass
class MockMessage:
    """
    Mocks the information contained in Telegram's Message class for tests.
    """

    message_id: int
    chat_id: int
    chat: MockChat
    text: str
    sticker: Optional[MockSticker] = None


@dataclass
class MockUpdate:
    """
    Mocks the information contained in Telegram's Update class for tests.
    """

    chat: MockChat
    message: MockMessage


@dataclass
class MockContextBot:
    """
    Mocks Telegram's context bot for tests. This class handles most of the
    logic in charge of sending messages and photos through a Telegram bot.
    """

    # tuple of (intended_chat_id, sent_message)
    messages: List[Tuple[int, str]] = field(default_factory=list)

    # tuple of (intended_chat_id, intented_reply_to_message_id, photo, caption)
    photos: List[Tuple[int, int, str, str]] = field(default_factory=list)

    def send_message(self, chat_id, text):
        """
        Pretends that a message is sent, instead stores it on an instance
        level for further checks on tests.
        """

        self.messages.append((chat_id, text))

    def send_photo(self, chat_id, reply_to_message_id, photo, caption):
        """
        Pretends that a message with a photo is sent, instead stores it
        on an instance level for further checks on tests.
        """

        self.photos.append((chat_id, reply_to_message_id, photo, caption))


@dataclass
class MockContext:
    """
    Mocks Telegram's Context class for tests.
    """

    bot: MockContextBot


@dataclass
class MockResponse:
    """
    Mock class to use instead of `requests` own response, to
    avoid making live requests during tests.
    """

    url: str

    def json(self):
        """
        Return a dictionary with test data, depending on the instance url
        """

        if self.url == DOGS_API_DOG_PICTURE_URL:
            return {
                "message": "https://dog.pics/dog.png"
            }

        if self.url == RANDOMFOX_API_URL:
            return {
                "image": "https://fox.pics/fox.png"
            }

        if self.url == DOGS_API_BREED_LIST_URL:
            return {
                "message": {
                    "pug": [],
                    "collie": ["border"],
                    "dalmatian": [],
                }
            }

        if "breed" in self.url:
            return {
                "message": "https://dog.pics/specific-breed/dog.png"
            }

        raise NotImplementedError(
            "Test case not yet covered in `MockResponse`"
        )


def get_mock_bot(monkeypatch: pytest.MonkeyPatch):
    """
    Helper function that initializes and returns a mocked instance of the
    DogPicsBot class, that can be safely used for tests.
    """

    monkeypatch.setenv("DPB_TG_TOKEN", "TEST_TOKEN_-_INVALID")
    monkeypatch.setattr("bot.Updater", MockUpdater)
    monkeypatch.setattr("requests.get", MockResponse)
    return DogPicsBot()


def get_mock_update(
    message="This is a message",
    chat_type=TELEGRAM_CHAT_TYPE_GROUP,
    is_sticker=False,
    emoji=None,
):
    """
    Given chat and message information, returns an instance of MockUpdate.
    """

    chat = MockChat(type=chat_type)

    return MockUpdate(
        message=MockMessage(
            message_id=randint(0, 100000),
            chat_id=randint(0, 100000),
            chat=chat,
            text=message,
            sticker=MockSticker(emoji=emoji) if is_sticker else None,
        ),
        chat=chat,
    )


def get_mock_context():
    """
    Returns a properly created instance of MockContext.
    """

    return MockContext(bot=MockContextBot())


# Code of actual tests
def test_get_random_dog_sound(monkeypatch: pytest.MonkeyPatch):
    """
    Unit test to verify that the bot is able to generate a random
    caption if needed.
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)

    # repeating the test several times
    test_iterations = max(len(DOG_SOUNDS) * 5, 25)
    for _ in range(test_iterations):
        assert bot.get_random_dog_sound() in DOG_SOUNDS


def test_show_help(monkeypatch: pytest.MonkeyPatch):
    """
    Unit test to verify that the bot is sending the proper help information
    when needed.
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)
    update = get_mock_update()
    context = get_mock_context()

    # context is empty
    assert len(context.bot.messages) == 0

    bot.show_help(update, context)

    # one message sent through context
    assert len(context.bot.messages) == 1

    # the tuple contains the chat_id and the message, we only care about
    # the message on this test
    _, sent_message = context.bot.messages[0]
    expected_message = (
        "If you want a dog picture, send me a message or "
        "use the /dog command."
    )
    assert expected_message in sent_message


def test_handle_text_messages_for_personal_message(
    monkeypatch: pytest.MonkeyPatch
):
    """
    Unit test to make sure that the bot always replies with a dog picture
    if messaged on a personal (non-group) chat
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)
    update = get_mock_update(chat_type="personal")
    context = get_mock_context()

    # context is empty of sent photos
    assert len(context.bot.photos) == 0

    bot.handle_text_messages(update, context)

    # one picture sent through context
    assert len(context.bot.photos) == 1

    # contains the chat_id, original message id, photo url and caption
    chat_id, reply_to_message_id, photo_url, caption = context.bot.photos[0]
    assert chat_id == update.message.chat_id
    assert reply_to_message_id == update.message.message_id
    assert photo_url == "https://dog.pics/dog.png"
    assert caption in DOG_SOUNDS


@pytest.mark.parametrize(
    "dog_message",
    [
        "I really like dogs",
        "Dogs go woof",
        "woof woof",
        "I have a new pup",
        "I have a new pupper",
        "tengo un perro",
        "mira mi lomito",
        "look a doggo",
        "look! a! doggo!",
        "puppy!",
        "woof!",
    ]
)
def test_handle_text_messages_for_group_message_with_dogs(
    monkeypatch: pytest.MonkeyPatch, dog_message: str
):
    """
    Unit test to verify that the bot properly sends a dog picture if
    a message that contains a dog reference is sent to a group chat.
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)
    update = get_mock_update(
        chat_type=TELEGRAM_CHAT_TYPE_GROUP, message=dog_message
    )
    context = get_mock_context()

    # context is empty of sent photos
    assert len(context.bot.photos) == 0

    bot.handle_text_messages(update, context)

    # one picture sent through context
    assert len(context.bot.photos) == 1

    # contains the chat_id, original message id, photo url and caption
    chat_id, reply_to_message_id, photo_url, caption = context.bot.photos[0]
    assert chat_id == update.message.chat_id
    assert reply_to_message_id == update.message.message_id
    assert photo_url == "https://dog.pics/dog.png"
    assert caption in DOG_SOUNDS


def test_handle_text_messages_for_group_message_without_dogs(
    monkeypatch: pytest.MonkeyPatch
):
    """
    Unit test to verify that the bot does not send a dog picture if
    a message sent to a group chat doesn't contain a dog reference.
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)
    update = get_mock_update(
        chat_type=TELEGRAM_CHAT_TYPE_GROUP, message="I really like plants",
    )
    context = get_mock_context()

    # context is empty of sent photos
    assert len(context.bot.photos) == 0

    bot.handle_text_messages(update, context)

    # context is still empty!
    assert len(context.bot.photos) == 0


@pytest.mark.parametrize(
    "sad_message",
    [
        "sad",
        "i'm really sad right now",
        "😢",
        "mano, estoy triste",
    ]
)
def test_handle_text_messages_for_sad_message(
    monkeypatch: pytest.MonkeyPatch, sad_message: str
):
    """
    Unit test to verify that, in the presence of a sad trigger within a
    message, the bot replies with a dog picture and a particular caption.
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)
    update = get_mock_update(message=sad_message)
    context = get_mock_context()

    # context is empty of sent photos
    assert len(context.bot.photos) == 0

    bot.handle_text_messages(update, context)

    # one picture sent through context
    assert len(context.bot.photos) == 1

    # contains the chat_id, original message id, photo url and caption
    chat_id, reply_to_message_id, photo_url, caption = context.bot.photos[0]
    assert chat_id == update.message.chat_id
    assert reply_to_message_id == update.message.message_id
    assert photo_url == "https://dog.pics/dog.png"
    assert caption == "Don't be sad, have a cute dog!"


def test_handle_text_messages_for_breed_message(
    monkeypatch: pytest.MonkeyPatch
):
    """
    Unit test to verify that, in the presence of a breed name within a
    message, the bot replies with a specific dog picture and a generic caption.
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)
    update = get_mock_update(message="i have a pug at home")
    context = get_mock_context()

    # context is empty of sent photos
    assert len(context.bot.photos) == 0

    bot.handle_text_messages(update, context)

    # one picture sent through context
    assert len(context.bot.photos) == 1

    # contains the chat_id, original message id, photo url and caption
    chat_id, reply_to_message_id, photo_url, caption = context.bot.photos[0]
    assert chat_id == update.message.chat_id
    assert reply_to_message_id == update.message.message_id
    assert photo_url == "https://dog.pics/specific-breed/dog.png"
    assert caption in DOG_SOUNDS


@pytest.mark.parametrize(
    "dog_emoji",
    [
        "🐶",
        "🐕",
        "🐩",
        "🌭",
    ]
)
def test_handle_text_messages_for_dog_sticker(
    monkeypatch: pytest.MonkeyPatch, dog_emoji: str
):
    """
    Unit test to verify that, in the presence of a sticker associated to a
    dog emoji, the bot replies with a random dog picture and a generic caption
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)
    update = get_mock_update(is_sticker=True, emoji=dog_emoji)
    context = get_mock_context()

    # context is empty of sent photos
    assert len(context.bot.photos) == 0

    bot.handle_stickers(update, context)

    # one picture sent through context
    assert len(context.bot.photos) == 1

    # contains the chat_id, original message id, photo url and caption
    chat_id, reply_to_message_id, photo_url, caption = context.bot.photos[0]
    assert chat_id == update.message.chat_id
    assert reply_to_message_id == update.message.message_id
    assert photo_url == "https://dog.pics/dog.png"
    assert caption in DOG_SOUNDS


@pytest.mark.parametrize(
    "fox_message",
    [
        "🦊",
        "me gusta mucho este animal 🦊",
        "foxes are the best",
        "i saw a fennec the other day",
        "do you have a fox?",
    ]
)
def test_handle_text_messages_for_fox_reference(
    monkeypatch: pytest.MonkeyPatch, fox_message: str
):
    """
    Unit test to verify that, in the presence of a message with a fox
    reference, the bot replies with a random fox picture and a specific
    caption.
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)
    update = get_mock_update(message=fox_message)
    context = get_mock_context()

    # context is empty of sent photos
    assert len(context.bot.photos) == 0

    bot.handle_text_messages(update, context)

    # one picture sent through context
    assert len(context.bot.photos) == 1

    # contains the chat_id, original message id, photo url and caption
    chat_id, reply_to_message_id, photo_url, caption = context.bot.photos[0]
    assert chat_id == update.message.chat_id
    assert reply_to_message_id == update.message.message_id
    assert photo_url == "https://fox.pics/fox.png"
    assert caption == "Yip yip!"
