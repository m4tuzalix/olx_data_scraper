class Data_scraper():
    def __init__(self, source, soup):
        self.source = source    
        self.soup = soup
    def get_location(self):
            try:
                location = self.source.xpath("*//a[@class='show-map-link']//strong/text()")
                if len(location[0]) == 0:
                    raise Exception
            except:
                location = self.source.xpath("*//a[@class='css-12hd9gg']/text()")
            finally:
                return location[0]
    def get_space(self):
        try:
            space = self.source.xpath("*//table[@class='details fixed marginbott20 margintop5 full']//tr[3]//td[1]//td//strong/text()")
            if len(space) > 0:
                clear_space = str(space[0]).strip().split(" ")
                space = clear_space[0]
            else:
                raise Exception
        except:
            space = self.source.xpath("//section[@class='section-overview']//div[@class='css-1ci0qpi']//li[contains(text(), 'Powierzchnia')]//strong/text()")
            clear_space = str(space[0]).strip().split(" ")
            space = clear_space[0]
        finally:
            return space

    def get_rent(self):
        try:
            rent= self.source.xpath("*//table[@class='details fixed marginbott20 margintop5 full']//tr[4]//td[1]//td//strong/text()")
            if len(rent) > 0:
                clear_rent = str(rent[0]).strip().split(" ")
                rent = clear_rent[0]
            else:
                raise Exception
        except:
            rent = self.source.xpath("//section[@class='section-overview']//div[@class='css-1ci0qpi']//li[contains(text(), 'Czynsz')]//strong/text()")
            clear_rent = str(rent[0]).strip().split(" ")
            rent = clear_rent[0]
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
            description = self.source.xpath("*//section[@class='section-description']//div//p/text()")
        finally:
            description = [str(x).strip() for x in description]
            return description
    
    def get_images(self):
        images_div = self.soup.find_all("div", {"class":"tcenter img-item"})
        images = []
        if len(images_div) > 1:
            for div in images_div:
                try:
                    image = div.find("img")
                    images.append(image["src"])
                except:
                    continue
        else:
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
            div_title = self.soup.find("div", {"class":"css-d2oo9m"}).find("h1")
            title = str(div_title.text).strip()
        finally:
            return title

    def get_price(self):
        try:
            div_price = self.soup.find("div", {"class":"price-label"}).find("strong")
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