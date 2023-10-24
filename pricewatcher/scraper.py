import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Define user-agent header to mimic a web browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
}

# List of URLs to scrape
urls = [
    "https://www.toppreise.ch/preisvergleich/Buehnenequipment/BEAMZ-S2500-160503-p547900",
    "https://www.toppreise.ch/preisvergleich/Smartphones/GOOGLE-Pixel-8-128GB-Obsidian-p741379",
    "https://www.toppreise.ch/preisvergleich/Smartphones/APPLE-iPhone-15-128GB-Schwarz-MTP03ZD-A-p739106"
]

# Initialize an empty dictionary to store the data
price_data = {}

for url in urls:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the price container element
        price_container = soup.find("div", class_="priceContainer productPrice")
        price = price_container.find("div", class_="Plugin_Price").get_text(strip=True)
        currency = price_container.find('span', class_='currency').get_text().strip()

        # Extract product name from the URL without the "p" number
        product_name = url.split('/')[-1].replace('-p', ' p').replace('-', ' ')[:-8]

        # Add "CHF" to the price
        price_with_currency = f"{price} {currency}"

        price_data[product_name] = {
            "Price": price_with_currency,
            "URL": url  # Include the original URL
        }

    else:
        print(f"Failed to fetch data from {url}")

# Add timestamp
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Create a dictionary that includes the product prices and timestamp as separate key-value pairs
output_data = {
    "Products": price_data,
    "Timestamp": timestamp
}

# Save the data to a JSON file
with open("price_data.json", "w") as json_file:
    json.dump(output_data, json_file, indent=4)

print("Data saved to price_data.json")
