# Import library
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import datetime

class TurnBackHoaxAPI:

    def __init__(self):
        """ Search URL"""
        self.search_url = 'https://turnbackhoax.id'

    def build_search_url(self, query: str, page_number: int):
        """Untuk mencari berita yang sesuai dengan query dan mengambil sesuai dengan halamannya"""
        qr = f'/?s={query}'
        pg = f'/page/{page_number}'
        return self.search_url + pg + qr

    def scrape_articles(self, query: str, max_pages: int):
        """Inti Scraping"""
        data = []

        for page in range(1, max_pages + 1):
            if page == 1:
                url = self.build_search_url(query, 1)
            else:
                url = self.build_search_url(query, page)

            # Request URL
            page = requests.get(url)

            # Convert HTML to BeautifulSoup
            soup = bs(page.text, "html.parser")

            # Find all article data
            article = soup.findAll("div", "mh-loop-content mh-clearfix")

            for scraping in article:
                text = scraping.find("h3", "entry-title mh-loop-title").text.strip().split("\n")
                link = scraping.find("a", {"rel": "bookmark"})["href"]
                time = scraping.find("span", "mh-meta-date updated").text.strip().split("\n")
                waktu = datetime.date.today().strftime("%Y-%m-%d")
                
                # Menghapus kata "[SALAH]" dari judul berita
                title = text[0].replace('[SALAH]', '').strip()
                
                # Memasukkan data scraping ke dalam list data bersama dengan status berita hoax
                data.append([title, link, time[0], waktu, True])  # True menandakan bahwa berita ini adalah hoax

        # Membuat DataFrame dengan kolom "Title", "Link", "Time", dan "Berita Hoax"
        df = pd.DataFrame(data, columns=["Title", "Link", "Time", "Waktu_Scraping","Berita Hoax"])
        return df
