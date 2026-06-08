import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://quotes.toscrape.com/page/{}/"

def scrape_all_pages():
    quotes_data = []
    page = 1
    
    while True:
        print(f"🔍 Scraping page {page}...")
        response = requests.get(BASE_URL.format(page))
        soup = BeautifulSoup(response.text, "html.parser")
        
        quotes = soup.find_all("div", class_="quote")
        
        if not quotes:  # No more quotes, exit loop
            break
        
        for quote in quotes:
            text = quote.find("span", class_="text").get_text()
            author = quote.find("small", class_="author").get_text()
            tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
            
            quotes_data.append({
                "quote": text,
                "author": author,
                "tags": ", ".join(tags)
            })
        
        print(f"✅ Scraped page {page} with {len(quotes)} quotes.")
        page += 1
    
    # Save to Excel
    df = pd.DataFrame(quotes_data)
    df.to_excel("quotes_all_pages.xlsx", index=False)
    print(f"✅ Done! Scraped {len(quotes_data)} quotes → saved to quotes_all_pages.xlsx")

scrape_all_pages()