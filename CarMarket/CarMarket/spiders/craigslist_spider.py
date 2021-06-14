from requests.models import Response
import scrapy
import requests
from bs4 import BeautifulSoup

from CarMarket.items import CarmarketItem

class CraigslistSpider(scrapy.Spider):
    name = 'craig'
    start_urls = ['https://phoenix.craigslist.org/d/cars-trucks-by-owner/search/cto?postal=85249&search_distance=50']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', class_='result-image gallery')

        print(links[0])
        #Filtering a elements for the link text itself, which is under 'href'
        for i in range(len(links)):
            links[i] = links[i]['href']

        #Scraping info from each link, yielding info as dict
        item = CarmarketItem()
        for link in links:

            print('\n\n', 'LINK: ', link, '\n\n')

            car_page = requests.get(link)
            car_soup = BeautifulSoup(car_page.content, 'html.parser')
            attributes = car_soup.find_all('p', class_='attrgroup')
            car_properties = attributes[1]

            #Parsing car_properties and turning it into dict
            dicc = {}
            spans = car_properties.find_all('span')
            for span in spans:
                text = span.text.replace(' ', '')
                arr = text.split(':')
                #Exception: odometer property can read 'odometerrolledover', and because it lacks a ':', it will create an array with 1 index.
                if (len(arr) == 1): dicc.update({'odometer': 'rolledover'})
                else: dicc.update({arr[0]: arr[1]})
            car_properties = dicc

            #Selecting desirable properties in car_properties
            keys = car_properties.keys()

            odometer = ''         
            if 'odometer' in keys:
                odometer = car_properties['odometer']
            else:
                odometer = '?'

            paint_color = ''
            if 'paintcolor' in keys:
                paint_color = car_properties['paintcolor']
            else:
                paint_color = '?'

            title_status = ''
            if 'titlestatus' in keys:
                title_status = car_properties['titlestatus']
            else:
                title_status = '?'

            item['title']           = car_soup.find('span', id="titletextonly").text
            item['year_make_model'] = attributes[0].text.replace('\n', '')
            item['price']           = car_soup.find('span', class_="price").text
            item['odometer']        = odometer
            item['paintcolor']      = paint_color
            item['titlestatus']     = title_status

            yield item
            

# fck = CraigslistSpider()
# fck