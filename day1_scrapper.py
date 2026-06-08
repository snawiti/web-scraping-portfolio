import requests
from bs4 import BeautifulSoup
import pandas as pd

# We'll scrape quotes from this beginner-friendly practice site
URL = "https://quotes.toscrape.com"

def scrape_quotes():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    quotes_data = []
    
    quotes = soup.find_all("div", class_="quote")
    
    for quote in quotes:
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
        
        quotes_data.append({
            "quote": text,
            "author": author,
            "tags": ", ".join(tags)
        })
    
    # Save to Excel
    df = pd.DataFrame(quotes_data)
    df.to_excel("quotes.xlsx", index=False)
    print(f"✅ Done! Scraped {len(quotes_data)} quotes → saved to quotes.xlsx")

scrape_quotes()