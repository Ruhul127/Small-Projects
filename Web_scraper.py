import requests
from bs4 import BeautifulSoup
import time
import random

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
    
    def fetch_page(self):
        """Fetches page content and handles HTTP errors."""
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()  # Checks for HTTP errors
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")
            return None

    def parse_data(self, content):
        """Parses data from the web page using BeautifulSoup."""
        soup = BeautifulSoup(content, 'html.parser')
        data = []

        # This example assumes the target is scraping items in a container.
        # Customize the selectors based on the site's structure.
        items = soup.find_all('div', class_='item-container')  # Example selector
        for item in items:
            title = item.find('h2').get_text(strip=True) if item.find('h2') else 'No title'
            price = item.find('span', class_='price').get_text(strip=True) if item.find('span', class_='price') else 'No price'
            
            # Data validation: ensure essential fields are present
            if title and price:
                data.append({'title': title, 'price': price})
        
        return data

    def save_data(self, data):
        """Saves data to a CSV file."""
        import csv
        with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['title', 'price'])
            writer.writeheader()
            writer.writerows(data)
        print("Data saved to scraped_data.csv")

    def scrape(self):
        """Main function to execute the scraping process."""
        print(f"Starting scrape for URL: {self.url}")
        content = self.fetch_page()
        
        if content:
            print("Parsing data...")
            data = self.parse_data(content)
            if data:
                self.save_data(data)
            else:
                print("No data found to save.")
        else:
            print("Failed to retrieve content.")

# Usage
if __name__ == "__main__":
    url = "www.example.com"  # Replace with the actual URL
    scraper = WebScraper(url)
    scraper.scrape()
