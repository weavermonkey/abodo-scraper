import requests
from bs4 import BeautifulSoup
import json
from utils import ReturnHTML,ListingsFromPage,DetailsFromListing

pin_codes = ['60603','60607']
property_details = {'60603':[],'60607':[]}

final_json_keys = ['property_name','property_address','lat_long','property_bedrooms','property_bathrooms','property_size','property_details','amenities']
for curr_code in pin_codes:
  while(len(property_details[curr_code]) <= 200):
    curr_home_page = ReturnHTML(curr_code).adobo_html
    listings = ListingsFromPage(curr_home_page).listing_urls
    for curr_listing in listings:
      listing_details = DetailsFromListing(curr_listing)
      if listing_details.property_pin_code == curr_code:
        curr_prop_details = { curr_key: vars(listing_details)[curr_key] for curr_key in final_json_keys }
        property_details[curr_code].append(curr_prop_details)
    for curr_pin_code in pin_codes:
      file_name = curr_pin_code+'.json'
      with open(file_name,'w') as json_op_file:
        json.dump(property_details[curr_pin_code],json_op_file)
