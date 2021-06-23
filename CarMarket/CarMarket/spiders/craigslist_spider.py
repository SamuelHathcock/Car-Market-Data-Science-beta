from typing import Dict
from requests.models import Response
import scrapy
import requests
from bs4 import BeautifulSoup

from CarMarket.items import CarmarketItem
from scrapy.loader import ItemLoader

class CraigslistSpider(scrapy.Spider):
    name = 'craig'
    start_urls = ['https://phoenix.craigslist.org/d/cars-trucks-by-owner/search/cto?postal=85249&search_distance=50']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', class_='result-image gallery')

        #Filtering a elements for the link text itself, which is under 'href'
        for i in range(len(links)):
            links[i] = links[i]['href']

        #Scraping info from each link, yielding info as Item
        item = CarmarketItem()
        for link in links:
            print('\n')
            scrape_count = self.crawler.stats.get_value('item_scraped_count')
            if scrape_count == 20: break

            car_page = requests.get(link)
            car_soup = BeautifulSoup(car_page.content, 'html.parser')
            attributes = car_soup.find_all('p', class_='attrgroup')

            #Finding car properties, parsing them and turning into dict
            car_properties = attributes[1]
            car_properties = parse_spans(car_properties)

            l = ItemLoader(item=CarmarketItem())

            l.add_value('title', car_soup.find('span', id="titletextonly").text)
            l.add_value('year_make_model', attributes[0].text)
            l.add_value('price', car_soup.find('span', class_="price").text)
            l.add_value('odometer', get_odometer(car_properties))
            l.add_value('paintcolor', get_paint_color(car_properties) )
            l.add_value('titlestatus', get_title_status(car_properties))
            
            yield l.load_item()

def parse_spans(car_properties):
    dicc = {}
    spans = car_properties.find_all('span')
    for span in spans:
        text = span.text.replace(' ', '')
        arr = text.split(':')
        #Exception: odometer property can read 'odometerrolledover', and because it lacks a ':', it will create an array with 1 index.
        if (len(arr) == 1): dicc.update({'odometer': 'rolledover'})
        else: dicc.update({arr[0]: arr[1]})
    return dicc

def get_odometer(car_properties: dict):
    if 'odometer' in car_properties:
        return car_properties['odometer']
    return '?'

def get_paint_color(car_properties: dict):
    if 'paintcolor' in car_properties:
        return car_properties['paintcolor']
    return '?'

def get_title_status(car_properties: dict):
    if 'titlestatus' in car_properties:
        return car_properties['titlestatus']
    return '?'