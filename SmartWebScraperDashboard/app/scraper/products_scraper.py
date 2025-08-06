import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_products():
    url = "https://books.toscrape.com/catalogue/page-1.html"
    base_url = "https://books.toscrape.com/catalogue/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    products = []

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Failed to fetch product page.")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.select('article.product_pod')

        for book in books:
            try:
                title = book.h3.a['title']
                price = book.select_one('.price_color').get_text(strip=True)
                availability = book.select_one('.availability').get_text(strip=True)
                relative_link = book.h3.a['href']
                product_link = base_url + relative_link

                products.append({
                    'title': title,
                    'price': price,
                    'availability': availability,
                    'link': product_link
                })

            except Exception as e:
                print(f"Error parsing product: {e}")
                continue

        # Check for next page
        next_btn = soup.select_one('li.next > a')
        if next_btn:
            next_page = next_btn['href']
            url = "https://books.toscrape.com/catalogue/" + next_page
        else:
            break

    # Save to JSON
    os.makedirs("data", exist_ok=True)
    with open("data/products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2)

    return products
