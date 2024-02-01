import os
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
import time
# from asgiref.sync import async_to_sync
import asyncio


DATA_DIR = "data"
STANDINGS_DIR = os.path.join(DATA_DIR, "standings")
SCORES_DIR = os.path.join(DATA_DIR, "scores")


# Function to grab html information from the url
async def get_html(url, selector, sleep=5, retries=5):
    html = None
    for i in range(1, retries + 1):
        time.sleep(sleep * i)

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                print(await page.title())
                html = await page.inner_html(selector)

        except PlaywrightTimeout:
            print(f"Timeout error on {url}")
            continue
        else:
            break

    return html


# Function to scrape season information
async def scrape_season(season):
    url = f"https://www.basketball-reference.com/leagues/NBA_{season}_games.html"
    html = await get_html(url, "#content .filter")

    soup = BeautifulSoup(html)
    links = soup.find_all("a")
    href = [l["href"] for l in links]
    standings_pages = [f"https://basketball-reference.com{l}" for l in href]

    for url in standings_pages:
        save_path = os.path.join(STANDINGS_DIR, url.split("/")[-1])
        if os.path.exists(save_path):
            continue

        html = await get_html(url, "#all_schedule")
        with open(save_path, "w+") as f:
            f.write(html)


# Function to scrape each individual game
async def scrape_game(standings_file):
    with open(standings_file, 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html)
    links = soup.find_all("a")
    hrefs = [l.get("href") for l in links]
    box_scores = [l for l in hrefs if l and "boxscore" in l and ".html" in l]
    box_scores = [f"https://www.basketball-reference.com{l}" for l in box_scores]

    for url in box_scores:
        save_path = os.path.join(SCORES_DIR, url.split("/")[-1])
        if os.path.exists(save_path):
            continue

        html = await get_html(url, "#content")
        if not html:
            continue

        with open(save_path, "w+") as f:
            f.write(html)


# @async_to_sync
# async def scrape_season(SEASONS):
#     for season in SEASONS:
#         await scrape_season(season)
#
#     standings_files = os.listdir(STANDINGS_DIR)
#
#     standings_files = [s for s in standings_files if ".html" in s]
#
#     for f in standings_files:
#         filepath = os.path.join(STANDINGS_DIR, f)
#         await scrape_game(filepath)
#
# SEASONS = list(range(2017, 2024))
#
# for season in SEASONS:
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(scrape_season(season))
#     loop.close()
#
# standings_files = os.listdir(STANDINGS_DIR)
# standings_files = [s for s in standings_files if ".html" in s]
#
# for f in standings_files:
#     filepath = os.path.join(STANDINGS_DIR, f)
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(scrape_game(filepath))
#     loop.close()

# scrape_data(list(range(2017, 2024)))

if __name__ == "__main__":
    SEASONS = list(range(2021, 2025))
    # asyncio.run(scrape_season(2024))
    for season in SEASONS:
        asyncio.run(scrape_season(season))

    standings_files = os.listdir(STANDINGS_DIR)
    standings_files = [s for s in standings_files if ".html" in s]
    #
    for f in standings_files:
        filepath = os.path.join(STANDINGS_DIR, f)
        asyncio.run(scrape_game(filepath))

