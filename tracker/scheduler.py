import schedule
import time
import django
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "price_tracker.settings")
django.setup()

from tracker.tasks import run_price_check

schedule.every(1).minutes.do(run_price_check)

print("Price Tracker Bot Running...")
while True:
    schedule.run_pending()
    time.sleep(1)
