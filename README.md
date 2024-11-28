# Telegram Bot for Tracking Used Cars on Auto.RIA

This project is a Python-based Telegram bot that scrapes car listings from [Auto.RIA](https://auto.ria.com/) and sends notifications about new cars or updates (e.g., price changes) to a Telegram channel. The bot includes features like database integration, scheduling, and real-time updates for price changes.

---

## Features

- **Car Listings Scraper**:
  - Fetches car listings from Auto.RIA based on specific filters.
  - Sends detailed car information to a Telegram channel, including photos, price, mileage, and location.

- **Database Integration**:
  - Uses SQLite to store car details, track unique cars, and handle price change notifications.

- **Real-Time Updates**:
  - Notifies when:
    - A new car matches the criteria.
    - The price of an existing car changes.
  - Replies to the original Telegram message with price updates.

- **Scheduling**:
  - Runs the scraper every 10 minutes to fetch the latest car listings.

---

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- SQLite (bundled with Python)
- Telegram bot token from [BotFather](https://core.telegram.org/bots#botfather)

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/telegram-auto-ria-bot.git
   cd telegram-auto-ria-bot
   ```
2. **Set Up a Virtual Environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up Environment Variables**:
   Create a .env file in the project root.
   Add the following variables to the .env file:
   ```bash
    BOT_TOKEN=your-telegram-bot-token
    CHANNEL_ID=@your-telegram-channel-id
   ```
5. **Start the bot**:
   ```bash
   python main.py
   ```

