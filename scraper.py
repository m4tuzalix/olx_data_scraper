from bs4 import BeautifulSoup
import requests
from lxml import html
from data_scraper import Data_scraper
from Excel import Excel

class Scraper():
    def __init__(self, city, rooms, price_start, price_end, page):
        self.city = city
        self.rooms = rooms
        self.price_start = price_start
        self.price_end = price_end
        self.page = page
        url = f"https://www.olx.pl/nieruchomosci/mieszkania/wynajem/{self.city}/?search%5Bfilter_float_price%3Afrom%5D={self.price_start}&search%5Bfilter_float_price%3Ato%5D={self.price_end}&search%5Bfilter_enum_rooms%5D%5B0%5D={self.rooms}&page={self.page}"
        source = requests.get(url).text
        self.soup = BeautifulSoup(source, "lxml")
    
    def page_amount(self):
        pages = self.soup.find_all("span", {"class":"item fleft"})
        page = pages[len(pages)-1].text
        return int(page)

    def get_all_adverts(self):
        adverts = self.soup.find_all("h3", {"class":"lheight22 margintop5"})
        links = []
        for a in adverts:
            element = a.find("a")
            links.append(element["href"])
        return links
    
    def get_adverts_data(self, links):
        for link in links:
            url = requests.get(link)
            source = html.fromstring(url.content)
            soup = BeautifulSoup(url.text, "lxml")
            scraper_main = Data_scraper(source, soup)
            data_array = [link, scraper_main.get_title(), 
                scraper_main.get_location(), scraper_main.get_space(), 
                scraper_main.get_rent(), scraper_main.get_price(),
                scraper_main.get_description(),scraper_main.get_images()]
            input_data = [str(x) for x in data_array]
            add_data_to_excel = Excel()
            add_data_to_excel.add_data(input_data)
        return True
            

if __name__ == "__main__":
    city = "wroclaw"
    rooms = "two"
    price_start = "1400"
    price_end = "2000"
    page = "1"
    scraper_main = Scraper(city,rooms,price_start,price_end,page) #// declared for the first time to get the number of pages
    pages = scraper_main.page_amount()
    for x in range(1,10,1):
        scraper_main = Scraper(city,rooms,price_start,price_end,x) #// declared again but this time under the loop which iterates the pages
        links = scraper_main.get_all_adverts()
        get_data = scraper_main.get_adverts_data(links)
        
