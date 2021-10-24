import pytest
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from bot import DogPicsBot

# Mocking Telegram's API
@dataclass
class MockDispatcher:
    handler_names: List[str] = field(default_factory=list)

    def add_handler(self, handler):
        self.handler_names.append(handler.__name__)


@dataclass
class MockUpdater:
    token: str
    use_context: bool = True
    dispatcher: MockDispatcher = MockDispatcher()

    def start_polling(self):
        return

@dataclass
class MockChat:
    type: str


@dataclass
class MockSticker:
    emoji: Optional[str] = None


@dataclass
class MockMessage:
    text: str
    chat_id: int = 1234
    message_id: int = 5678
    sticker: Optional[MockSticker] = None


@dataclass
class MockUpdate:
    message: MockMessage
    chat: MockChat

@dataclass
class MockContextBot:
    # tuple of (intended_chat_id, sent_message)
    messages: List[Tuple[int, str]] = field(default_factory=list)

    def send_message(self, chat_id, text):
        self.messages.append((chat_id, text))

@dataclass
class MockContext:
    bot: MockContextBot


def get_mock_bot(monkeypatch):
    monkeypatch.setattr("bot.Updater", MockUpdater)
    monkeypatch.setenv("DPB_TG_TOKEN", "TEST_TOKEN_-_INVALID")
    return DogPicsBot()


def get_mock_update(
    message="This is a message", type="group", is_sticker=False, emoji=None
):
    return MockUpdate(
        message=MockMessage(
            text=message,
            sticker=MockSticker(emoji=emoji) if is_sticker else None,
        ),
        chat=MockChat(type=type)
    )


def get_mock_context():
    return MockContext(bot=MockContextBot())


# Code of actual tests
def test_get_random_dog_sound(monkeypatch):
    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)

    # repeating the test several times
    test_iterations = 10
    for _ in range(test_iterations):
        assert bot.get_random_dog_sound() in DogPicsBot.dog_sounds


def test_show_help(monkeypatch):
    # instantiating mock bot
    bot = get_mock_bot(monkeypatch)
    update = get_mock_update()
    context = get_mock_context()

    # context is empty
    assert len(context.bot.messages) == 0

    bot.show_help(update, context)

    # one message sent through context
    assert len(context.bot.messages) == 1

    # the tuple contains the chat_id and the message, we only care about the message on this test
    _, sent_message = context.bot.messages[0]
    assert "If you want a dog picture, send me a message or use the /dog command." in sent_message
