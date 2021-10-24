# Dog Pics Bot

A simple Telegram bot that sends random dog pictures (and more!).

You can test the bot on Telegram, just click here: [@DogPicsBot](https://t.me/dogpicsbot).

Currently on [v1.6.1](https://github.com/aitorres/dogpicsbot/releases/tag/v1.6.1). For more information about versions and changes, refer to the [changelog](CHANGELOG.md).

## Requirements

The bot runs on **Python 3** (officially supporting Python 3.7, 3.8 and 3.9), and depends on packages listed on the `requirements.txt` file.

For ease of use, you should create a Python 3 virtual environment and then use `pip` in order to install the requirements, with the following command:

```bash
pip install -r requirements.txt
```

If you're more onto using `conda`, the following command will create an environment, activate it and install the requirements:

```bash
conda create -n dogpicsbot python=3.7
conda activate dogpicsbot
pip install -r requirements.txt
```

## Installation

Simply clone this repository, fetch the requirements on a virtual environment as stated above and then set a new environment variable named `DPB_TG_TOKEN` with your Telegram bot API token. If you don't have a valid token, [check this out](https://core.telegram.org/bots).

Note that one feature (sending dog pictures freely through group chats on certain trigger words) requires the bot's Privacy Mode to be **disabled** (this can be done through @BotFather).

## Usage

Run the following command on a command line. It will keep the polling thread running (therefore keeping your bot alive) until you kill the process.

```bash
python bot.py
```

## Test

Unit tests for the bot are found in the [tests.py](tests.py) file. You can run them after setting up your local environment with the following command:

```bash
pytest -v tests.py
```

## What's next

The next features to be developed are:

- Let the dog detect and reply to images that contain dogs in them ([reference](https://towardsdatascience.com/a-dog-detector-and-breed-classifier-4feb99e1f852))
- Replying "intelligently" to messages relating to dogs (e.g. emotions)
- Explore the use of other dog pics APIs
- Drop support for Python 3.7 and add support for Python 3.10
- And more!

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.
