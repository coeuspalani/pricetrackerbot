from django.core.exceptions import ObjectDoesNotExist
from .models import TrackedProduct
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from urllib.parse import urlparse
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def send_email(product, price, receiver_email, url):
    sender_email = "retre.platform@gmail.com"
    app_password = "pkvbthukammwlllu"
    subject = f"Price Drop Alert: ₹{price} for {product[:30]}..."
    body = f"""Good news!\n\nThe price of "{product}" has dropped to ₹{price}.\nCheck it here: {url}\n\n– Price Tracker Bot"""
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent!")
    except Exception as e:
        print("Email failed:", e)

def run_price_check():
    products = TrackedProduct.objects.all()
    for item in products:
        try:
            session = requests.Session()
            session.headers.update(HEADERS)
            response = session.get(item.product_url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            final_url = response.url
            soup = BeautifulSoup(response.content, "html.parser")
            hostname = urlparse(final_url).hostname.lower()
            with open("debug_myntra.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            title_tag, price_tag = None, None

            if "amazon" in hostname:
                title_tag = soup.find(id="productTitle")
                price_tag = soup.find("span", class_="a-price-whole")
            elif "flipkart" in hostname:
                title_tag = soup.find("span",class_="VU-ZEz")
                price_tag = soup.find("div",class_=["Nx9bqj","CxhGGd"])
            #elif "meesho" in hostname:
             #   title_tag = soup.find("h1", class_="sc-eDvSVe fhfLdV")
              #  price_tag = soup.find("h4", class_="sc-eDvSVe biMVPh")
            #elif "ajio" in hostname: #website blocked, forbidden (provide this after adding selenium)
             #   title_tag = soup.find("h1", class_="prod-name")
              #  price_tag = soup.find("div", class_="prod-sp")

            if not title_tag or not price_tag:
                print(f"[-] Skipping: Missing title or price for {item.product_url}")
                with open("debug_failed.html", "w", encoding="utf-8") as f:
                    f.write(soup.prettify())
                continue

            title = title_tag.get_text(strip=True)
            price_text = price_tag.get_text(strip=True)
            clean_price = price_text.replace(",", "").replace("₹", "").replace("Rs", "").strip()

            try:
                current_price = int(float(clean_price))
            except ValueError:
                print(f"[-] Price format error for {item.product_url}: '{clean_price}'")
                continue

            print(f"{title} → Rs.{current_price}")

            if current_price <= item.target_price:
                send_email(title, current_price, item.email, item.product_url)
                item.delete()

            df = pd.DataFrame({
                "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "Product": [title],
                "Price (INR)": [current_price]
            })
            df.to_csv("price_history.csv", mode="a", header=not pd.io.common.file_exists("price_history.csv"), index=False)

        except Timeout:
            print(f"[-] Timeout while checking: {item.product_url}")
        except ConnectionError:
            print(f"[-] Connection error — check internet: {item.product_url}")
        except HTTPError as http_err:
            print(f"[-] HTTP error for {item.product_url}: {http_err}")
        except RequestException as req_err:
            print(f"[-] Request failed for {item.product_url}: {req_err}")
        except ObjectDoesNotExist:
            print(f"[-] Product entry no longer exists in DB.")
        except Exception as e:
            print(f"[!] Unexpected error: {e}")
