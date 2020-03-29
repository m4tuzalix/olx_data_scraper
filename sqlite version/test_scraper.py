from scraper import Scraper
import unittest

class Test_Scraper(unittest.TestCase):
    @classmethod
    def setUpClass(start):
        city = "wroclaw"
        rooms = "two"
        price_start = "1400"
        price_end = "2000"
        page = "1"
        start.scraper_main = Scraper(city,rooms,price_start,price_end,page)
        
    @classmethod
    def tearDownClass(finish):
        print("finished")

    def test01_page_amount(self):
        pages = self.scraper_main.page_amount()
        self.assertIsInstance(pages, int)
    
    def test02_all_adverts(self):
        adverts = self.scraper_main.get_all_adverts()
        self.assertIsInstance(adverts, list)
        self.assertGreater(len(adverts), 0)
    
    def test_03_adverts_data(self):
        link = ["https://www.olx.pl/oferta/mieszkanie-na-wynajem-wroclaw-popowice-bialowieska-33-m2-przytulne-CID3-IDDjYVW.html#6757b534ce;promoted"]
        adverts = self.scraper_main.get_adverts_data(link)
        self.assertTrue(adverts)