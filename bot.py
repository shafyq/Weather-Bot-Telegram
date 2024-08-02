import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import pytz
from datetime import datetime, timedelta

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a few command handlers
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    context.user_data['referral_code'] = 'YOUR_REFERRAL_CODE'  # Change this to your referral code logic
    update.message.reply_text('Hi! Please enter your referral code.')

def check_referral(update: Update, context: CallbackContext) -> None:
    if update.message.text == context.user_data['referral_code']:
        update.message.reply_text('Referral code accepted! What should I call you?')
        context.user_data['verified'] = True
    else:
        update.message.reply_text('Invalid referral code. Please try again.')

def set_name(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('verified'):
        context.user_data['name'] = update.message.text
        update.message.reply_text(f'Nice to meet you, {context.user_data["name"]}! Please share your location.')
    else:
        update.message.reply_text('Please enter a valid referral code first.')

def set_location(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('verified'):
        context.user_data['location'] = update.message.text
        update.message.reply_text('Location set! You will receive daily weather updates at 6 AM.')
        # Adjust timezone and schedule tasks
    else:
        update.message.reply_text('Please enter a valid referral code first.')

def good_morning(context: CallbackContext) -> None:
    job = context.job
    name = context.user_data.get('name', 'there')
    location = context.user_data.get('location')
    weather_info = get_weather(location)
    context.bot.send_message(job.context, text=f'Good morning, {name}!\n{weather_info}')

def get_weather(location: str) -> str:
    api_key = 'YOUR_WEATHER_API_KEY'
    url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&hours=24'
    response = requests.get(url)
    weather_data = response.json()
    # Format the weather data
    return "Weather data here"  # Replace with actual formatted data

def main() -> None:
    updater = Updater("YOUR_TELEGRAM_API_TOKEN")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_referral))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r'^[A-Za-z]+$'), set_name))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r'^[A-Za-z, ]+$'), set_location))

    updater.job_queue.run_daily(good_morning, time=datetime.time(6, 0, 0))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
