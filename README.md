# Dog Pics Bot

A simple Telegram bot that sends random dog pictures (and more!).

You can test the bot on Telegram, just click here: [@DogPicsBot](https://t.me/dogpicsbot).

Currently on [v1.7.0](https://github.com/aitorres/dogpicsbot/releases/tag/v1.7.0). For more information about versions and changes, refer to the [changelog](CHANGELOG.md).

## Requirements

The bot runs on **Python 3** (officially supporting Python 3.9 to 3.12), and depends on packages listed on the `requirements.txt` file.

For ease of use, use [`poetry`](https://python-poetry.org/) to install dependencies with the following command:

```bash
poetry install
```

## Installation

Simply clone this repository, install the requirements with `poetry` then set a new environment variable named `DPB_TG_TOKEN` with your Telegram bot API token. If you don't have a valid token, [check out this guide](https://core.telegram.org/bots).

Note that one feature (sending dog pictures freely through group chats on certain trigger words) requires the bot's Privacy Mode to be **disabled** (this can be done through @BotFather).

## Usage

Run the following command on a command line. It will keep the polling thread running (therefore keeping your bot alive) until you kill the process.

```bash
poetry run python bot.py
```

## Test

Unit tests for the bot are found in the [tests.py](tests.py) file. You can run them with verbose output after setting up your local environment, including the 80% coverage check that is expected of the repository, with the following command:

```bash
poetry run pytest
```

## What's next

The next features to be developed are:

- Let the dog detect and reply to images that contain dogs in them ([reference](https://towardsdatascience.com/a-dog-detector-and-breed-classifier-4feb99e1f852))
- Replying "intelligently" to messages relating to dogs (e.g. emotions)
- Explore the use of other dog pics APIs
- And more!

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

All contributions that involve changing the codebase should either include or update [tests](tests.py), and make sure that all tests pass before changes can be merged to the `master` branch.

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.
