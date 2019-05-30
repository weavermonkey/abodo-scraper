import requests
from bs4 import BeautifulSoup

class ReturnHTML():
    def __init__(__self__,pin_code):
        self.base_url = 'https://www.abodo.com/chicago-il?lat=41.8817767&lng=-87.6371461'
        self.abodo_url = self.base_url+pin_code+'Chicago, IL'
        self.adobo_html = BeautifulSoup(requests.get(self.adobo_url).text,'lxml')

class ListingsFromPage():
    def __init__(__self__,abodo_soup_obj):
        self.listings = soup_obj.findAll('section',{'class':'search-section search-section-rent-report-page'})[0].findAll('div',{'class':'flex-split-view-left-side'})[0].findAll('div',{'class':'market-tab-content'})[0].findAll('div',{'id':'market-search'})[0].findAll('div',{'class':'col-xs-12 no-pad'})[0].findAll('div',{'id':'list_holder_listings'})[0].findAll('div',{'id':'property-tile-grid-container'})[0].findAll('div',{'class':'property-tile-grid '})[0]
        self.listing_urls = []
        for curr_listing in listings:
            append_url = i.findAll('div')[0].contents[1].findAll('div',{'class':'grid-text grid-property-name row grid-property-name-row'})[0].findAll('a')[0]['href']
            self.listing_urls.append(append_url)

class DetailsFromListing():
    def __init__(__self__,listing_url):
        self.listing_soup_obj = BeautifulSoup(requests.get(listing_url).text,'lxml')
