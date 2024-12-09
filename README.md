# Iron-Sentinel

Iron Sentinel is the vigilant guardian of the Black Iron Company. Managing operations, ranks, logistics, and roleplay, Iron Sentinel ensures the regiment runs like a well-oiled machine, always ready to rise, fight, and conquer.

## Features

- **Message Moderation**: Automatically moderates messages using OpenAI's Moderation API to ensure appropriate content.
- **Logging**: Logs actions taken by the bot to a specified log channel for transparency and review.
- **Extensible**: Easily add new features and cogs to extend the bot's functionality.

## Setup

### Prerequisites

- Python 3.8+
- Discord bot token
- OpenAI API key

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/Iron-Sentinel.git
    cd Iron-Sentinel
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv .venv
    # On Windows
    .\.venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your environment variables:

    ```env
    DISCORD_BOT_TOKEN="your_discord_bot_token"
    OPENAI_API_KEY="your_openai_api_key"
    ```

5. Update the `channel_config.py` file with your log channel name:

    ```python
    # channel_config.py

    channel_config = {
        # Server Management
        "logs": "your-log-channel-name"
    }
    ```

### Running the Bot

1. Run the bot:

    ```sh
    python main.py
    ```

## Usage

- The bot will automatically moderate messages in the specified channels and log any actions taken to the log channel.
- Customize the bot by adding new cogs and features as needed.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
