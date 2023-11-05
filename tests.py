"""
Unit tests for the functions and classes implemented for the DogPicsBot.

@author Andrés Ignacio Torres <andresitorresm@gmail.com>
"""

from dataclasses import dataclass, field
from random import randint
from typing import List, Optional, Tuple

import pytest

from bot import (
    DOG_SOUNDS,
    DOGS_API_BREED_LIST_URL,
    DOGS_API_DOG_PICTURE_URL,
    FOX_SOUNDS,
    RANDOMFOX_API_URL,
    TELEGRAM_CHAT_TYPE_GROUP,
    WOLF_PICTURES,
    DogPicsBot,
)


# Mocking Telegram's API
@dataclass
class MockApplication:
    """
    Mock class to bypass Telegram's application on tests.
    """

    _token: str = ""
    handler_names: List[str] = field(default_factory=list)

    def build(self):
        """
        Fakes the process in which a Telegram bot is built.
        """

        return self

    def token(self, _token: str):
        """
        Fakes the process in which a Telegram bot's token is set.
        """

        self._token = _token
        return self

    @staticmethod
    def builder():
        """
        Fakes the process in which a Telegram bot's builder is set.
        """

        return MockApplication()

    def add_handler(self, handler):
        """
        Fakes the process in which a new handler is added to a Telegram
        bot's dispatcher. Instead, stores the name of the new handler
        on an instance level for further checks on tests.
        """

        self.handler_names.append(str(handler.__class__))

    def run_polling(self):
        """
        Fakes the call to Telegram's application's start_polling, but in reality
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
    timeout: int

    def json(self):
        """
        Return a dictionary with test data, depending on the instance url
        """

        if self.url == DOGS_API_DOG_PICTURE_URL:
            return {"message": "https://dog.pics/dog.png"}

        if self.url == RANDOMFOX_API_URL:
            return {"image": "https://fox.pics/fox.png"}

        if self.url == DOGS_API_BREED_LIST_URL:
            return {
                "message": {
                    "pug": [],
                    "collie": ["border"],
                    "dalmatian": [],
                }
            }

        if "breed" in self.url:
            return {"message": "https://dog.pics/specific-breed/dog.png"}

        raise NotImplementedError("Test case not yet covered in `MockResponse`")


def get_mock_bot(monkeypatch: pytest.MonkeyPatch):
    """
    Helper function that initializes and returns a mocked instance of the
    DogPicsBot class, that can be safely used for tests.
    """

    monkeypatch.setenv("DPB_TG_TOKEN", "TEST_TOKEN_-_INVALID")
    monkeypatch.setattr("bot.Application", MockApplication)
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
async def test_get_random_dog_sound(monkeypatch: pytest.MonkeyPatch):
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


async def test_get_random_fox_sound(monkeypatch: pytest.MonkeyPatch):
    """
    Unit test to verify that the bot is able to generate a random
    caption if needed.
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)

    # repeating the test several times
    test_iterations = max(len(FOX_SOUNDS) * 5, 25)
    for _ in range(test_iterations):
        assert bot.get_random_fox_sound() in FOX_SOUNDS


async def test_get_random_wolf_picture(monkeypatch: pytest.MonkeyPatch):
    """
    Unit test to verify that the bot is able to generate a random
    wolf picture if needed.
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)

    # repeating the test several times
    test_iterations = max(len(WOLF_PICTURES) * 5, 25)
    for _ in range(test_iterations):
        assert bot.get_random_wolf_picture() in WOLF_PICTURES


async def test_show_help(monkeypatch: pytest.MonkeyPatch):
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

    await bot.show_help(update, context)

    # one message sent through context
    assert len(context.bot.messages) == 1

    # the tuple contains the chat_id and the message, we only care about
    # the message on this test
    _, sent_message = context.bot.messages[0]
    expected_message = "If you want a dog picture, send me a message or use the /dog command."
    assert expected_message in sent_message


async def test_handle_text_messages_for_private_message(monkeypatch: pytest.MonkeyPatch):
    """
    Unit test to make sure that the bot always replies with a dog picture
    if messaged on a private (non-group) chat
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)
    update = get_mock_update(chat_type="private")
    context = get_mock_context()

    # context is empty of sent photos
    assert len(context.bot.photos) == 0

    await bot.handle_text_messages(update, context)

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
        "pooch!",
    ],
)
async def test_handle_text_messages_for_group_message_with_dogs(
    monkeypatch: pytest.MonkeyPatch, dog_message: str
):
    """
    Unit test to verify that the bot properly sends a dog picture if
    a message that contains a dog reference is sent to a group chat.
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)
    update = get_mock_update(chat_type=TELEGRAM_CHAT_TYPE_GROUP, message=dog_message)
    context = get_mock_context()

    # context is empty of sent photos
    assert len(context.bot.photos) == 0

    await bot.handle_text_messages(update, context)

    # one picture sent through context
    assert len(context.bot.photos) == 1

    # contains the chat_id, original message id, photo url and caption
    chat_id, reply_to_message_id, photo_url, caption = context.bot.photos[0]
    assert chat_id == update.message.chat_id
    assert reply_to_message_id == update.message.message_id
    assert photo_url == "https://dog.pics/dog.png"
    assert caption in DOG_SOUNDS


async def test_handle_text_messages_for_group_message_without_dogs(monkeypatch: pytest.MonkeyPatch):
    """
    Unit test to verify that the bot does not send a dog picture if
    a message sent to a group chat doesn't contain a dog reference.
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)
    update = get_mock_update(
        chat_type=TELEGRAM_CHAT_TYPE_GROUP,
        message="I really like plants",
    )
    context = get_mock_context()

    # context is empty of sent photos
    assert len(context.bot.photos) == 0

    await bot.handle_text_messages(update, context)

    # context is still empty!
    assert len(context.bot.photos) == 0


@pytest.mark.parametrize(
    "sad_message",
    [
        "sad",
        "i'm really sad right now",
        "😢",
        "😭😓",
        "She left me 💔",
        "I'm not gonna make it 😞",
        "mano, estoy triste",
        "estoy despechado",
        "ando deprimido",
        "tengo tusa",
    ],
)
async def test_handle_text_messages_for_sad_message(
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

    await bot.handle_text_messages(update, context)

    # one picture sent through context
    assert len(context.bot.photos) == 1

    # contains the chat_id, original message id, photo url and caption
    chat_id, reply_to_message_id, photo_url, caption = context.bot.photos[0]
    assert chat_id == update.message.chat_id
    assert reply_to_message_id == update.message.message_id
    assert photo_url == "https://dog.pics/dog.png"
    assert caption == "Don't be sad, have a cute dog!"


@pytest.mark.parametrize(
    "msg",
    [
        "i have a pug at home",
        "i have two pugs at home",
        "this is pugtastic!",
    ],
)
async def test_handle_text_messages_for_breed_message(monkeypatch: pytest.MonkeyPatch, msg: str):
    """
    Unit test to verify that, in the presence of a breed name within a
    message, the bot replies with a specific dog picture and a generic caption.
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)
    update = get_mock_update(message=msg)
    context = get_mock_context()

    # context is empty of sent photos
    assert len(context.bot.photos) == 0

    await bot.handle_text_messages(update, context)

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
    ],
)
async def test_handle_text_messages_for_dog_sticker(
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

    await bot.handle_stickers(update, context)

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
        "mira un zorro!",
    ],
)
async def test_handle_text_messages_for_fox_reference(
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

    await bot.handle_text_messages(update, context)

    # one picture sent through context
    assert len(context.bot.photos) == 1

    # contains the chat_id, original message id, photo url and caption
    chat_id, reply_to_message_id, photo_url, caption = context.bot.photos[0]
    assert chat_id == update.message.chat_id
    assert reply_to_message_id == update.message.message_id
    assert photo_url == "https://fox.pics/fox.png"
    assert caption in FOX_SOUNDS


@pytest.mark.parametrize(
    "wolf_message",
    [
        "🐺",
        "me gusta mucho este animal 🐺",
        "wolves are the best",
        "is that a wolf?",
        "¡mira un lobo!",
        "howl howl howl!",
    ],
)
async def test_handle_text_messages_for_wolf_reference(
    monkeypatch: pytest.MonkeyPatch, wolf_message: str
):
    """
    Unit test to verify that, in the presence of a message with a wolf
    reference, the bot replies with a random wolf picture and a specific
    caption.
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)
    update = get_mock_update(message=wolf_message)
    context = get_mock_context()

    # context is empty of sent photos
    assert len(context.bot.photos) == 0

    await bot.handle_text_messages(update, context)

    # one picture sent through context
    assert len(context.bot.photos) == 1

    # contains the chat_id, original message id, photo url and caption
    chat_id, reply_to_message_id, photo_url, caption = context.bot.photos[0]
    assert chat_id == update.message.chat_id
    assert reply_to_message_id == update.message.message_id
    assert photo_url in WOLF_PICTURES
    assert caption == "Howl!"


async def test_bot_fails_without_telegram_bot_token_in_environment(monkeypatch: pytest.MonkeyPatch):
    """
    Unit test to verify that the bot properly raises an exception if
    it's initialized in an environment that doesn't have a proper
    Telegram Bot token set up as an env var.
    """

    monkeypatch.setenv("DPB_TG_TOKEN", "")
    with pytest.raises(RuntimeError, match="FATAL: No token was found."):
        DogPicsBot()


async def test_run_bot(monkeypatch: pytest.MonkeyPatch):
    """
    Unit test to verify that all expected bot handlers are initialized
    properly when calling the `run_bot` method.
    """

    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)

    assert len(bot.application.handler_names) == 0
    bot.run_bot()

    # ? we're actually only checking that we got the right amount
    # ? of handlers, and that their underlining classes are
    # ? added in order; we might be able to actually check names or more
    # ? information with either some introspection or attribute checks,
    # ? but it might not be needed for now

    assert len(bot.application.handler_names) == 5
    assert bot.application.handler_names == [
        # /start
        "<class 'telegram.ext._commandhandler.CommandHandler'>",
        # /help
        "<class 'telegram.ext._commandhandler.CommandHandler'>",
        # /dog
        "<class 'telegram.ext._commandhandler.CommandHandler'>",
        # text messages
        "<class 'telegram.ext._messagehandler.MessageHandler'>",
        # stickers
        "<class 'telegram.ext._messagehandler.MessageHandler'>",
    ]
