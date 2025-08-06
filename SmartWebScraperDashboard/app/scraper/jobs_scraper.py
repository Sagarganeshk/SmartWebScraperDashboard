import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_jobs():
    url = "https://remoteok.com/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch jobs.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []

    for job in soup.select('tr.job'):
        try:
            title = job.select_one('h2').get_text(strip=True)
            company = job.select_one('.companyLink > h3').get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in job.select('.tag')]
            date = job.select_one('time')
            date = date['datetime'] if date else "N/A"
            link = "https://remoteok.com" + job['data-href']

            jobs.append({
                'title': title,
                'company': company,
                'tags': tags,
                'date': date,
                'link': link
            })
        except Exception as e:
            print(f"Error parsing job: {e}")
            continue

    # Save to JSON
    os.makedirs("data", exist_ok=True)
    with open("data/jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

    return jobs
