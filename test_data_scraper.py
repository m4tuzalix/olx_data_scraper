import unittest
import requests
from lxml import html
from data_scraper import Data_scraper
from bs4 import BeautifulSoup
class Test_Date_Scraper(unittest.TestCase):

    @classmethod
    def setUpClass(start):
        url = "https://www.olx.pl/oferta/mieszkanie-na-wynajem-wroclaw-popowice-bialowieska-33-m2-przytulne-CID3-IDDjYVW.html#6757b534ce;promoted"
        r = requests.get(url)
        tree = html.fromstring(r.content)
        soup = BeautifulSoup(r.text, "lxml")
        start.scraper = Data_scraper(tree, soup)
    
    @classmethod
    def tearDownClass(finish):
        print("finished")
    
    def test00_location(self):
        location = self.scraper.get_location()
        self.assertIn("Wrocław", location)
    
    def test01_space(self):
        space = self.scraper.get_space()
        try:
            intVal = int(space)
        except ValueError:
            intVal = None
        self.assertIsNotNone(intVal)

    def test02_rent(self):
        space = self.scraper.get_rent()
        try:
            intVal = int(space)
        except ValueError:
            intVal = None
        self.assertIsNotNone(intVal)

    def test03_price(self):
        price = self.scraper.get_price()
        try:
            intVal = int(price)
        except ValueError:
            intVal = None
        self.assertIsNotNone(intVal)
    
    def test04_images(self):
        images = self.scraper.get_images()
        self.assertIsInstance(images, list)
        self.assertGreater(len(images), 0)

    def test05_title(self):
        title = self.scraper.get_title()
        self.assertGreater(len(title), 0)

    def test06_description(self):
        description= self.scraper.get_description()
        self.assertIsInstance(description, list)
        self.assertGreater(len(description), 0)

