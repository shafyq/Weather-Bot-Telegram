import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import pytz
from datetime import datetime, time, timedelta

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a few command handlers
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    context.user_data['referral_code'] = 'Ho11@Ho11@'  # Change this to your referral code logic
    update.message.reply_text('Hi! This is private Bot. Please give your secret code')

def check_referral(update: Update, context: CallbackContext) -> None:
    if update.message.text == context.user_data['referral_code']:
        update.message.reply_text('Secret code accepted! What should I call you?')
        context.user_data['verified'] = True
    else:
        update.message.reply_text('Invalid Secret code. Please try again.')

def set_name(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('verified'):
        context.user_data['name'] = update.message.text
        update.message.reply_text(f'Nice to meet you, {context.user_data["name"]}! Please share your location.')
    else:
        update.message.reply_text('Please enter a valid secret code first.')

def set_location(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('verified'):
        context.user_data['location'] = update.message.text
        update.message.reply_text('Location set! You will receive daily weather updates at 6 AM.')
        # Adjust timezone and schedule tasks
    else:
        update.message.reply_text('Please enter a valid secret code first.')

def good_morning(context: CallbackContext) -> None:
    job = context.job
    name = context.user_data.get('name', 'there')
    location = context.user_data.get('location')
    weather_info = get_weather(location)
    context.bot.send_message(job.context, text=f'Good morning, {name}!\n{weather_info}')

def get_weather(location: str) -> str:
    api_key = 'c56366569f234c13919192259242807'
    url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&hours=24'
    response = requests.get(url)
    weather_data = response.json()
    # Format the weather data
    return "Weather data here"  # Replace with actual formatted data

def shut_down(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('verified'):
        context.user_data['shut_down'] = True
        update.message.reply_text('Bot shut down for you. You will no longer receive messages.')
    else:
        update.message.reply_text('Please enter a valid secret code first.')

def main() -> None:
    updater = Updater("7419238901:AAFw1seutpi2Pi4KVhm_3G0vrjn7CzN5cCE")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_referral))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r'^[A-Za-z]+$'), set_name))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r'^[A-Za-z, ]+$'), set_location))
    dispatcher.add_handler(CommandHandler("shutdown", shut_down))

    def daily_job(context: CallbackContext):
        for user_id, user_data in context.dispatcher.user_data.items():
            if not user_data.get('shut_down', False):
                context.job_queue.run_once(good_morning, time(6, 0, 0), context=user_id, name=str(user_id))

    updater.job_queue.run_daily(daily_job, time=time(6, 0, 0))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
