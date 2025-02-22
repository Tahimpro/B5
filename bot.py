import asyncio
from pyrogram import Client
from scraper import get_latest_movies, get_howblogs_link, get_hubdrive_link, get_final_download_link
from info import API_ID, API_HASH, BOT_TOKEN, CHANNEL_ID, SKY_MOVIES_URL, CHECK_INTERVAL, POST_GAP

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def scrape_and_send():
    processed_links = set()
    
    while True:
        latest_movies = get_latest_movies()
        for movie in latest_movies:
            movie_url = f"{SKY_MOVIES_URL}{movie}"
            if movie_url in processed_links:
                continue  # Skip already processed movies
            
            howblogs_link = get_howblogs_link(movie_url)
            if not howblogs_link:
                continue
            
            hubdrive_link = get_hubdrive_link(howblogs_link)
            if not hubdrive_link:
                continue
            
            final_link = get_final_download_link(hubdrive_link)
            if final_link:
                await app.send_message(CHANNEL_ID, f"/l {final_link}")
                processed_links.add(movie_url)
                
                # Wait 3 minutes before sending the next link
                await asyncio.sleep(POST_GAP)

        await asyncio.sleep(CHECK_INTERVAL)  # Wait 5 minutes before checking again

@app.on_message()
async def start_scraping(client, message):
    if message.text.lower() == "/start":
        await message.reply("Bot is running and scraping every 5 minutes.")

app.start()
asyncio.run(scrape_and_send())  # Start scraping automatically
