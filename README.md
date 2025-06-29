
# Price Tracker Bot (Django)

This is a Django-based web application that allows users to track product prices from major e-commerce platforms and receive email alerts when prices drop below a specified target. The project aims to help users make smarter purchasing decisions by notifying them when a product becomes more affordable.

## Features

- Supports tracking from the following platforms:
  - Amazon
  - Flipkart
  - Meesho
  - Myntra
  - Ajio
- Allows users to input:
  - Product URL
  - Desired price
  - Email address for notifications
- Scrapes real-time product pricing
- Sends automated email alerts when the current price is less than or equal to the desired price
- Clean and responsive web interface using Bootstrap and custom CSS

## Technology Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, Bootstrap, CSS
- **Web scraping:** Requests, BeautifulSoup
- **Email Alerts:** SMTP (configured in Django)
- **Database:** SQLite (default Django DB)
- **Scheduler (optional):** Cron jobs or Celery for periodic checks

## How It Works

1. The user enters a product URL, their target price, and email.
2. The app fetches the current price of the product from the provided URL.
3. If the current price is equal to or less than the target, an email notification is sent.
4. The data is stored for future checks and analysis (if periodic scheduling is enabled).

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/price-tracker-bot.git
cd price-tracker-bot
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Email Settings
Open `settings.py` and update the following:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yourprovider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Start the Server
```bash
python manage.py runserver
```

Open your browser and go to: `http://127.0.0.1:8000/`





## Contributions

This project is a personal initiative to explore web scraping, email automation, and Django web development. Suggestions and contributions are welcome.

## Disclaimer

This project is intended for educational purposes. Use it responsibly and be aware of the scraping policies of each e-commerce website.
