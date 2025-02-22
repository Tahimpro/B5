import time
import requests
from bs4 import BeautifulSoup
from pyrogram import Client
import re

# ✅ Telegram UserBot Configuration
API_ID = "YOUR_API_ID"  
API_HASH = "YOUR_API_HASH"  
CHAT_ID = "YOUR_PRIVATE_CHANNEL_ID"  # Private Telegram Channel

# ✅ Pyrogram UserBot (Sessionless)
app = Client("userbot", api_id=API_ID, api_hash=API_HASH)

# ✅ Custom Headers to Avoid Blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

BASE_URL = "https://skymovieshd.video/"
CHECK_INTERVAL = 300  # Scrape every 5 minutes
POST_INTERVAL = 180   # 3-minute gap between posts

def get_movie_links():
    """Scrape movie links from SkyMoviesHD."""
    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        movie_links = []
        for link in soup.find_all("a", href=True):
            url = link["href"]
            if "https://howblogs.xyz/" in url:
                movie_links.append(url)

        return list(set(movie_links))  # Remove duplicates
    except Exception as e:
        print(f"Error fetching SkyMoviesHD: {e}")
        return []

def get_hubdrive_link(blog_url):
    """Extract the HubDrive link from the HowBlogs page."""
    try:
        response = requests.get(blog_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a", href=True):
            url = link["href"]
            if "hubdrive.dad" in url:
                return url
        return None
    except Exception as e:
        print(f"Error fetching HowBlogs: {e}")
        return None

def get_final_download_link(hubdrive_url):
    """Extract the direct download link from HubDrive."""
    try:
        response = requests.get(hubdrive_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for button in soup.find_all("a", text=re.compile(r"Direct|Instant Download", re.I)):
            return button["href"]
        return None
    except Exception as e:
        print(f"Error fetching HubDrive: {e}")
        return None

def send_to_telegram(download_link):
    """Send the final link to the private Telegram channel."""
    with app:
        message = f"/l {download_link}"
        app.send_message(CHAT_ID, message)
        print(f"✅ Sent to Telegram: {download_link}")

def main():
    """Main loop to scrape and send links."""
    while True:
        print("🔄 Checking for new movies...")
        movie_links = get_movie_links()

        for blog_url in movie_links:
            hubdrive_url = get_hubdrive_link(blog_url)
            if not hubdrive_url:
                continue

            final_link = get_final_download_link(hubdrive_url)
            if final_link:
                send_to_telegram(final_link)
                time.sleep(POST_INTERVAL)  # Wait 3 minutes before sending the next link

        print("⏳ Sleeping for 5 minutes...")
        time.sleep(CHECK_INTERVAL)  # Wait 5 minutes before checking again

if __name__ == "__main__":
    main()
