import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_news():
    url = "https://www.ndtv.com/latest"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch news.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    news_cards = soup.select(".news_Itm")

    news_list = []

    for card in news_cards:
        try:
            headline_tag = card.select_one(".newsHdng a")
            headline = headline_tag.get_text(strip=True)
            link = headline_tag['href']
            summary_tag = card.select_one(".newsCont")
            summary = summary_tag.get_text(strip=True) if summary_tag else "No summary"

            news_list.append({
                "headline": headline,
                "summary": summary,
                "link": link
            })
        except Exception as e:
            print(f"Error parsing news: {e}")
            continue

    # Save to JSON
    os.makedirs("data", exist_ok=True)
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(news_list, f, indent=2)

    return news_list
