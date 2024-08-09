# Telegram Session Converter

This project is a tool for converting Telegram `tdata` session files into Pyrogram session strings, validating the sessions, and organizing them into valid and invalid categories.

## Features
- **Convert `tdata` folders**: Converts Telegram `tdata` session data into Pyrogram session strings.
- **Session validation**: Validates if the Telegram session is active and usable.
- **Organized output**: Automatically sorts sessions into `valid` and `invalid` folders.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/telegram-session-converter.git
    cd telegram-session-converter
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the configuration:
    - Update the `config.json` file with your Telegram API credentials (`api_id`, `api_hash`).

## Usage

1. Place your Telegram `tdata` folders into the `input` directory.

2. Run the converter:
    ```bash
    python converter.py
    ```

3. After execution, the `tdata` folders will be moved to the `output/valid` or `output/invalid` directories based on their validation status.

## Project Structure

- **converter.py**: Main script that handles the conversion, validation, and organization of Telegram sessions.
- **input/**: Directory where you should place your `tdata` folders for processing.
- **output/valid/**: Directory where valid sessions are stored.
- **output/invalid/**: Directory where invalid sessions are stored.
- **log.txt**: Log file that contains details of the conversion and validation process.

## Logging
All operations are logged in the `log.txt` file, providing detailed information on the status of each processed session.

