# Import library
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import datetime

class MetroNewsAPI:

    def __init__(self):
        """ Search URL"""
        self.search_url = 'https://www.metrotvnews.com'

    def build_search_url(self, query: str, page_number: int):
        """Untuk mencari berita yang sesuai dengan query dan mengambil sesuai dengan halamannya"""
        if page_number == 1:
            return f"{self.search_url}/search?query={query}"
        else:
            return f"{self.search_url}/search/{query}/{page_number}"

    def scrape_articles(self, query: str, max_pages: int):
        """Inti scraping"""
        data = []

        for page in range(1, max_pages + 1):
            url = self.build_search_url(query, page)

            # Request URL Website
            page = requests.get(url)

            # Parsing format HTML ke dalam BeautifulSoup
            soup = BeautifulSoup(page.text, "html.parser")

            # Memanggil judul artikel yang berada di luar
            article = soup.findAll("div", "item")

            # Mengambil judul artikel dan link
            for scraping in article:
                text = scraping.find("h3").text.strip().split("\n")
                link = scraping.find("a")["href"]
                keterangan = scraping.find("span").text.strip().split("\n")
                updater = re.match(r'(.+?)\s•', keterangan[0]).group(1)
                waktu = datetime.date.today().strftime("%Y-%m-%d")

                data.append([text[0], link, updater, waktu, False])  # Memasukkan data scraping ke dalam list data

        # Membuat DataFrame
        df = pd.DataFrame(data, columns=["Judul Artikel", "Link", "Team", "Waktu_Scraping", "Berita_Hoax"])
        return df
