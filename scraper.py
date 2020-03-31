from bs4 import BeautifulSoup
import requests
from lxml import html
from data_scraper import Data_scraper
from Excel import Excel
from database import Database
from colorama import Fore, init
init()

class Scraper(Database):
    def __init__(self, city, rooms, price_start, price_end, page):
        Database.__init__(self)
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

    def get_all_adverts(self, mode):
        adverts = self.soup.find_all("td", {"class":"offer"})
        links = [] #// all adverts which will be passed to scrap
        for a in adverts:
            try:
                element = a.find("a", {"data-cy":"listing-ad-title"})
                link = element["href"]
                double_check = self.check_db(link) #// checks if link is already present in database
                if double_check:
                    if mode == 1:
                        date = a.find_all("small", {"class":"breadcrumb x-normal"})
                        if "dzisiaj" in str(date[2].find("span").text):
                            links.append(link)
                            self.add_links(link) #// adds link to database
                    elif mode == 2:
                        links.append(link)
                        self.add_links(link)
                    else:
                        print(Fore.RED+"Please provide the correct mode: 1 or 2")
                        break
            except Exception as e:
                print(f'{Fore.YELLOW} {e}')
                continue
        self.close() #// close the connection
        return links
    
    def get_adverts_data(self, links):
        if len(links) > 0:
            print(f"{Fore.LIGHTMAGENTA_EX} scraping page: {self.page}")
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
        print(Fore.GREEN+"Haven't detected new adverts")
        return False

if __name__ == "__main__":
    city = "wroclaw"
    rooms = "two"
    price_start = "1400"
    price_end = "2000"
    page = "1"
    mode = 1 #//// two modes: 1 for the latest, 2 for everything
    DATABSE = Database().db_main() #/// checkes database is exists and clears it
    scraper_main = Scraper(city,rooms,price_start,price_end,page) #// declared for the first time to get the number of pages
    pages = scraper_main.page_amount()
    print(Fore.GREEN+"started work")
    for x in range(1,pages-1,1):
        scraper_main = Scraper(city,rooms,price_start,price_end,x) #// declared again but this time under the loop which iterates the pages
        links = scraper_main.get_all_adverts(mode) 
        get_data = scraper_main.get_adverts_data(links)
        if get_data == False:
            break
    print(Fore.GREEN+"finished")
        
