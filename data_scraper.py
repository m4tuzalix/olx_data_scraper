class Data_scraper():
    def __init__(self, source, soup):
        self.source = source    
        self.soup = soup
    def get_location(self):
            try:
                location = self.source.xpath("*//div[@class='offer-user__address']//address//p/text()")
                if len(location[0]) == 0:
                    raise Exception
            except:
                try:
                    location = self.source.xpath("*//a[@class='css-12hd9gg']/text()")
                except:
                    location = ""
            finally:
                return location
    def get_space(self):
        try:
            space = self.source.xpath("*//ul[@class='offer-details']//li//span[@class='offer-details__param']//strong/text()")
            if len(space) > 0:
                clear_space = str(space[0]).strip().split(" ")
                space = clear_space[0]
            else:
                raise Exception
        except:
            try:
                space = self.source.xpath("//section[@class='section-overview']//div[@class='css-1ci0qpi']//li[contains(text(), 'Powierzchnia')]//strong/text()")
                clear_space = str(space[0]).strip().split(" ")
                space = clear_space[0]
            except:
                space = ""
        finally:
            return space

    def get_rent(self):
        try:
            rent = self.source.xpath("*//ul[@class='offer-details']//li//span[@class='offer-details__param']//strong/text()")
            if len(rent) > 0:
                clear_rent = str(rent[1]).strip().split(" ")
                rent = clear_rent[0]
            else:
                raise Exception
        except:
            try:
                rent = self.source.xpath("//section[@class='section-overview']//div[@class='css-1ci0qpi']//li[contains(text(), 'Czynsz')]//strong/text()")
                clear_rent = str(rent[0]).strip().split(" ")
                rent = clear_rent[0]
            except:
                rent = ""
        finally:
            return rent

    def get_description(self):
        try:
            description = self.source.xpath("//div[@class='clr lheight20 large']/text()")
            if len(description) > 0:
                pass
            else:
                raise Exception
        except:
            try:
                description = self.source.xpath("*//section[@class='section-description']//div//p/text()")
            except:
                description = ""
        finally:
            description = [str(x).strip() for x in description]
            return description
    
    def get_images(self):
        images = []
        try:
            images_div = self.soup.find('ul', {"id":"descGallery"}).find_all("a")
            for img in images_div:
                try:
                    images.append(img["href"])
                except:
                    continue
        except:
            images_figure = self.soup.find_all("figure", {"class":"thumbsItem"})
            for figure in images_figure:
                try:
                    image = figure.find("img")
                    src_index = str(image["src"]).index(";s")
                    images.append(image["src"][:src_index]+";s=644x461")
                except:
                    continue
        return images
    
    def get_title(self):
        try:
            div_title = self.soup.find("div", {"class":"offer-titlebox"}).find("h1")
            if div_title != None:
                title = str(div_title.text).strip()
            else:
                raise Exception
        except:
            try:
                div_title = self.soup.find("div", {"class":"css-d2oo9m"}).find("h1")
                title = str(div_title.text).strip()
            except:
                title = ""
        finally:
            return title

    def get_price(self):
        try:
            div_price = self.soup.find("div", {"class":"pricelabel"}).find("strong")
            if len(div_price) > 0:
                price = str(div_price.text[:-3]).replace(" ", "")
            else:
                raise Exception
        except:
            try:
                div_price = self.soup.find("div", {"class":"css-1vr19r7"})
                dummy_text = div_price.find("small").text
                price = str(div_price.text[:-len(dummy_text)-4]).replace(" ", "")
            except:
                price = ""
        finally:
            return price