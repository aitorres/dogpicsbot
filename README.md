# Dog Pics Bot

A simple Telegram bot that sends random dog pictures (and more!).

You can test the bot on Telegram, just click here: [@DogPicsBot](https://t.me/dogpicsbot).

Currently on [v1.4.1](https://github.com/aitorres/dogpicsbot/releases/tag/v1.3.0). For more information about versions and changes, refer to the [changelog](CHANGELOG.md).

## Requirements

The bot runs on `python 3` (developed and tested with `python 3.7.3` specifically), and uses the packages listed on the `requirements.txt` file.

For ease of use, you should create a Python 3 virtual environment and then use `pip` in order to install the requirements, with the following command:

```bash
pip install -r requirements.txt
```

## Installation

Simply clone this repository, fetch the requirements on a virtual environment as stated above and then set a new environment variable named `DPB_TG_TOKEN` with your Telegram bot API token. If you don't have a valid token, [check this out](https://core.telegram.org/bots).

Note that one feature (sending dog pictures freely through group chats on certain trigger words) requires the bot's Privacy Mode to be disabled (this can be done through @BotFather).

## Usage

Run the following command on a command line. It will keep the polling thread running (therefore keeping your bot alive) until you kill the process.

```bash
python bot.py
```

## What's next

The next features to be developed are:

- Replying "intelligently" to messages relating to dogs (e.g. emotions)
- Explore the use of other dog pics APIs
- Replying to sad messages with dog pictures :(
- And more!

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.
