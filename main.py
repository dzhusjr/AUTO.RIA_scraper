import requests
import telebot
from src.fetcher import fetch_cars
from src.db import init_db, get_existing_car, add_or_update_car, save_message_id
import schedule
import time
import os
import dotenv

dotenv.load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@testforvacancy"
SCHEDULE = 10 # minutes

bot = telebot.TeleBot(BOT_TOKEN)

def post_to_channel(car):
    media_group = []
    details_message = (
        f"[{car['title']}]({car['link']})\n"
        f"💵 {car['price']}\n"
        f"⚙️ {car['mileage']}\n"
        f"📍 {car['location']}\n"
    )
    for i, photo_url in enumerate(car['photos']):
        response = requests.get(photo_url, stream=True)
        if response.status_code == 200:
            media_group.append(
                telebot.types.InputMediaPhoto(response.content, caption=details_message if i == 0 else None, parse_mode="Markdown")
            )
        if len(media_group) >= 10:
            break

    if media_group:
        while True:
            try:
                # x = bot.send_message(CHANNEL_ID, f"[NEW CAR] {car['title']}")
                x = bot.send_media_group(CHANNEL_ID, media_group)
                save_message_id(car["link"], x[0].message_id)
                break
            except telebot.apihelper.ApiTelegramException as e:
                if e.error_code == 429:  # Too Many Requests
                    retry_after = int(e.result_json["parameters"]["retry_after"])
                    print(f"[WARNING] Rate limit exceeded. Retrying after {retry_after} seconds...")
                    time.sleep(retry_after)
                    post_to_channel(car)
                else:
                    print(f"[ERROR] Telegram API error: {e}, retrying...")
                    post_to_channel(car)

def scrape_and_notify(url):
    cars = fetch_cars(url)
    for car in cars:
        existing_car = get_existing_car(car["link"])
        if not existing_car:
            print(f"[NEW CAR] {car['title']} - {car['price']}")
            post_to_channel(car)
            add_or_update_car(car,False)
        else:
            # Check for price changes
            if existing_car[3] != car["price"]:  # Price column index is 3
                print(f"[PRICE CHANGE] {car['title']} - {car['price']} (was {existing_car[3]})")
                post_to_channel(car)
                add_or_update_car(car,True)

def run_scheduler():
    schedule.every(SCHEDULE).minutes.do(scrape_and_notify)

    print("[INFO] Scheduler started. Running every 10 minutes.")
    while True:
        try:
            schedule.run_pending()
            time.sleep(0.5)
        except:
            pass
if __name__ == "__main__":
    init_db()
    scrape_and_notify(url = "https://auto.ria.com/search/?indexName=auto,order_auto,newauto_search&categories.main.id=1&brand.id[0]=79&model.id[0]=2104&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=1&page=0&size=100")
    run_scheduler()
