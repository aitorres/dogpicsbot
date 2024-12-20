# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.1] - 2024-12-14

### Changed

- Sad message response probability can be read from the environment (.env file)
- Default value of sad message response probability is 1.0 to match the usual behavior (<v3.1.0)

## [3.1.0] - 2024-12-14

### Added

- A new variable is added to the main bot class to account for a "sad message probability", to potentially limit the amount of sad message responses

### Changed

- Added support for Python 3.13 on tests
- Updated Github Actions checks
- Dependency updates

## [3.0.0] - 2024-08-01

### Changed

- Dropped support for Python 3.9
- Removed certain logging statements to reduce unneeded logged information
- Tweak to sad keywords
- Minor updates

## [2.0.0] - 2023-11-05

### Added

- Official support for Python 3.12
- Upgrade `python-telegram-bot` from v13.* to v20.* and refactor bot to work in async calls

## [1.7.0] - 2023-11-05

### Added

- Environment variables can now be managed via `.env` files using `dotenv`
- Improve developer experience with `pre-commit`, `isort`, and other linting hooks
- Add auto-release action on CI/CD

### Changed

- Project dependencies are now managed with `poetry`
- Dropped official support for Python 3.8
- Minor refactors and style changes

## [1.6.3] - 2022-02-14

### Changed

- Breeds can now appear as substrings and will be matched accordingly

## [1.6.2] - 2021-10-24

### Added

- The bot now replies to wolf emojis and triggers with (a limited set of) wolf pictures! This was a community suggestion.

### Changed

- Minor refactor on the methods that query lists to get random elements

## [1.6.1] - 2021-10-24

### Changed

- Fixed a regression that made the bot incompatible with Python 3.7 after partial typing was added to the bot
- Reordered bot initialization statements in order to avoid hitting the API (in order to get the most recent list of breeds) if a Telegram bot token is not set.

## [1.6.0] - 2021-10-24

### Added

- More triggers for sad messages (e.g. `triste`, Spanish word for `sad`)
- New [tests](tests.py) module that contains mockups and unit tests in order to ensure that the bot runs properly at all times, and to prevent new functionalities and bug fixes from introducing unexpected behavior and bugs.
- Github Actions workflow set up in the repository in order to run tests automatically on every push, and requiring a minimum coverage of 80% in order to pass

### Changed

- Fixed variable names in order to follow Python standards and conventions (#11, thanks @seleregb)
- Refactored the handlers that send pictures in order to avoid code repetition (#14, thanks @seleregb)
- Dependencies in [requirements.txt](requirements.txt) have been updated and simplified to keep main dependencies only.
- The bot is now fired up directly when running `bot.py`, avoiding an intermediate call to a `main` function (that no longer exists)
- General code cleanup, refactoring and updates

## [1.5.3] - 2021-02-20

### Changed

- Fixed a regression bug in which Telegram supergrous were not being considered as groups, but as personal chats instead.

## [1.5.2] - 2021-01-23

### Changed

- Fixed a regression bug in which certain dog triggers were not matching as a prefix (e.g. "perro" was not being matched properly, but "perr" was).

## [1.5.1] - 2020-10-30

### Changed

- Fixed the way message words are compared to trigger words in order to reduce false positives. Contribution by [@german1608](https://github.com/german1608).
- Updated package dependencies, particularly to fix a security vulnerability by an old version of `cryptography`.

## [1.5.0] - 2020-10-10

### Added

- The bot is now also triggered by messages that might have a sad sentiment, and are replied to with a dog picture. Contribution by [@baspalinckx](https://github.com/baspalinckx)

## [1.4.2] - 2020-09-03

### Changed

- Reduced the amount of comparisons done while parsing each message by making sure only the radix of similar words is checked for appearance.

## [1.4.1] - 2020-08-23

### Changed

- Refactored use of the Random Fox API.
- Added support for two other dog trigger words (in Spanish).

## [1.4.0] - 2020-08-23

### Added

- Easter egg! The bot now supports _fox_ triggers and sends a fox image accordingly.

### Changed

- Added yet more support for dog / dog-related emoji.
- Relocated dog triggers for improved extensibility and readability.

## [1.3.1] - 2020-08-23

### Added

- The bot now randomly selects a "dog sound" (barking) phrase as the pics caption.
- A few more trigger words were added in order to automatically send a dog pic.

## [1.3.0] - 2020-01-27

### Added

- The bot is now able to detect and reply to certain dog breeds with a picture of that specific breed.

## [1.2.0] - 2020-01-19

### Added

- The bot is now able to detect and reply to dog-related stickers.

### Changed

- The bot now recognizes more trigger words, as well as dog-related emoji.
- Project dependencies have been updated.

## [1.1.0] - 2020-01-14

### Added

- The bot is now able to reply to certain trigger words in group chats, sending dog pictures.

## [1.0.2] - 2019-07-21

### Added

- [CHANGELOG.md](CHANGELOG.md) file to track changes between versions.
- List of planned features, soon to be developed, in [README.md](README.md) file.

### Removed

- Heroku config files (runtime.txt and Procfile)

## [1.0.1] - 2019-07-20

### Added

- [LICENSE](LICENSE) file.

### Fixed

- Medium-impact typo on the help message shown on bot startup or through the /help command.

## [1.0.0] - 2019-07-20

### Added

- Initial release of the Dog Pics Telegram bot.
