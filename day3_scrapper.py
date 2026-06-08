import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

# Convert word ratings to numbers
RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

def scrape_books():
    all_books = []
    page = 1

    while True:
        print(f"📦 Scraping page {page}...")
        response = requests.get(BASE_URL.format(page))

        # Stop if page doesn't exist
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").get_text().strip()
            rating_word = book.p["class"][1]
            rating = RATING_MAP.get(rating_word, 0)
            availability = book.find("p", class_="availability").get_text().strip()

            all_books.append({
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability
            })

        page += 1

    # Save to Excel with formatting
    df = pd.DataFrame(all_books)
    df.to_excel("books.xlsx", index=False)
    print(f"\n✅ Done! Scraped {len(all_books)} books across {page-1} pages → saved to books.xlsx")
    
    # Quick summary
    print(f"\n📊 Quick Stats:")
    print(f"   Average price: {df['price'].str.replace('Â£','£').iloc[0]}")
    print(f"   5-star books: {len(df[df['rating']==5])}")
    print(f"   In stock: {len(df[df['availability']=='In stock'])}")

scrape_books()