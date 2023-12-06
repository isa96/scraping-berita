import pandas as pd
from requests import get
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import datetime

class DetikNewsApi:

    def __init__(self):
        """ Search URL"""
        self.search_url = 'https://www.detik.com/search/searchall?'

    def build_search_url(self, query: str, page_number: int):
        """Untuk mencari berita yang sesuai dengan query dan mengambil sesuai dengan halamannya"""
        if page_number == 1:
            return f"{self.search_url}query={query}&siteid=2"
        else:
            return f"{self.search_url}query={query}&siteid=2&sortby=time&sorttime=0&page={page_number}"

    def scrape_articles(self, query: str, max_pages: int):
        data = []

        for page in range(1, max_pages + 1):
            url = self.build_search_url(query, page)

            # Request URL Website
            page = get(url)

            # Parsing format HTML ke dalam BeautifulSoup
            soup = BeautifulSoup(page.text, "html.parser")

            # Memanggil judul artikel yang berada di luar
            article = soup.findAll("article")

            # Mengambil judul artikel dan link
            for scraping in article:
                text = scraping.find("h2", "title").text.strip().split("\n")
                link = scraping.find("a")["href"]
                keterangan = scraping.find("span", "category")
                waktu = datetime.date.today().strftime("%Y-%m-%d")

                data.append([text[0], link, keterangan, waktu, False])  # Memasukkan data scraping ke dalam list data

        # Membuat DataFrame
        df = pd.DataFrame(data, columns=["Judul Artikel", "Link", "Team", "Waktu_Scraping", "Berita_Hoax"])
        return df
