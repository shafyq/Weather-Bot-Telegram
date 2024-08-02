# Weather-Bot-Telegram
A Telegram Bot that will provide 24 hours of weather in advance and will notify of weather changes or weather activities such as snow, rain, heatwave
# Telegram Weather Bot

This bot sends a good morning message every day at 6 AM along with the next 24 hours weather forecast. It also notifies users of any significant weather changes, such as rain or snow.

## Setup

1. Clone the repository to your DigitalOcean droplet.
2. Install necessary dependencies:
    ```sh
    sudo apt update
    sudo apt install python3 python3-pip
    pip3 install python-telegram-bot requests pytz
    ```
3. Replace placeholders in `bot.py` with your actual API keys and referral code logic.
4. Run the bot:
    ```sh
    python3 bot.py
    ```
5. Set up the bot to run as a service:
    ```sh
    sudo nano /etc/systemd/system/telegram_bot.service
    ```
    Add the following content:
    ```ini
    [Unit]
    Description=Telegram Bot
    After=network.target

    [Service]
    User=root
    WorkingDirectory=/path/to/your/telegram_bot
    ExecStart=/usr/bin/python3 /path/to/your/telegram_bot/bot.py
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
6. Enable and start the service:
    ```sh
    sudo systemctl enable telegram_bot
    sudo systemctl start telegram_bot
    ```

## Usage

- Start the bot by sending `/start`.
- Enter the referral code when prompted.
- Set your name and location.
- To shut down the bot for yourself, use the `/shutdown` command.

## Note

- The bot supports up to 2 cities.
- Ensure your location is in the correct format to get accurate weather data.
