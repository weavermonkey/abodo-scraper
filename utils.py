import requests
from bs4 import BeautifulSoup
import json

x = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
class ReturnHTML():
    def __init__(self,pin_code):
        self.pin_code_mapping = {'60607':'http://www.abodo.com/chicago-il?lat=41.8733696&lng=-87.6507140&place_name=60607%20Chicago,%20IL&zoom_level=12',
                                 '60603':'http://www.abodo.com/chicago-il?lat=41.8809155&lng=-87.6254251&place_name=60603%20Chicago,%20IL&zoom_level=12'
                                }
        self.base_url = self.pin_code_mapping[pin_code]
        self.adobo_html = BeautifulSoup(requests.get(self.base_url,headers=x).text,'lxml')
class ListingsFromPage():
    def __init__(self,abodo_soup_obj):
        self.listings = soup_obj.findAll('section',{'class':'search-section search-section-rent-report-page'})[0].findAll('div',{'class':'flex-split-view-left-side'})[0].findAll('div',{'class':'market-tab-content'})[0].findAll('div',{'id':'market-search'})[0].findAll('div',{'class':'col-xs-12 no-pad'})[0].findAll('div',{'id':'list_holder_listings'})[0].findAll('div',{'id':'property-tile-grid-container'})[0].findAll('div',{'class':'property-tile-grid '})[0]
        self.listing_urls = []
        for curr_listing in listings:
            append_url = curr_listing.findAll('div')[0].contents[1].findAll('div',{'class':'grid-text grid-property-name row grid-property-name-row'})[0].findAll('a')[0]['href']
            self.listing_urls.append(append_url)

class DetailsFromListing():
    def __init__(self,listing_url):
        self.listing_soup_obj = BeautifulSoup(requests.get(listing_url,headers=x).text,'lxml')
        self.js_script = json.loads((self.listing_soup_obj.findAll('div',{'class':'property-seo-links'})[0].findAll('script',{'type':'application/ld+json'})[0].text))
        self.property_pin_code = str(self.js_script['address']['postalCode'])
        self.property_basics()
        self.amenities = self.return_amenities()
    
    def return_amenities(self):
        amenities = []
        amenities_div = self.listing_soup_obj.findAll('div',{'class':'amenity-group property-page-text col-xs-12 col-sm-8 no-pad'})[1:]
        for curr_row in amenities_div:
            span_rows = curr_row.findAll('span')
            for curr_amenity in span_rows:
                try:
                    amenities.append(curr_amenity.find('span').text)
                except:
                    pass
                return amenities
    
    def property_basics(self):
        property_basics = self.listing_soup_obj.find('div',{'class':'content'})
        self.property_name = property_basics.find('h1',{'class':'property-headline'}).text.strip()
        self.prop_address = self.listing_soup_obj.findAll('span',{'class':'property-map-address'})[0]
        for index,val in enumerate(self.prop_address.stripped_strings):
            self.property_address =  val.strip().replace('\n','brrt').replace('  ','').replace('brrt',' ')
        self.lat_long = property_basics.find('div',{'id':'walkscore-map-pane'}).attrs['data-src'].split('&')[0].split('center=')[-1]
        self.property_bedrooms = property_basics.find('div',{'class':'listing-summary-detail'}).text.strip()
        self.property_bathrooms = property_basics.find('div',{'class':'listing-summary-bathrooms listing-summary-section'}).find('div',{'class':'listing-summary-detail'}).text.strip()
        self.property_size = property_basics.find('div',{'class':'listing-summary-unit-size listing-summary-section'}).find('div',{'class':'listing-summary-detail'}).text
        prop_det = property_basics.find('div',{'class':'content-row-info col-xs-12 col-sm-8 no-pad'}).find('div',{'class':'shortentext'}).stripped_strings
        text = []
        for index,val in enumerate(prop_det):
            text.append(val.replace('\t','').replace(u"\u2022",'').replace(u"\u2013",'-').replace(u"\u2019","'"))
        self.property_details = ' '.join(text)
