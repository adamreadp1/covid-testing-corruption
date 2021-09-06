import requests
import json
from bs4 import BeautifulSoup

api_key = '98800058-49c6-4c02-9b1a-74cffc1319c5'

for company in ['NL clinic', 'nl clinic']:
    company = company.lower() #-> ['nl', 'clinic'] -> nl+clinic
    response = requests.get(
        'https://api.company-information.service.gov.uk/search?items_per_page=1&q='+'+'.join(company.split()), 
        auth=(api_key, ''))
    response_json = response.json()
    company_found = response_json['items'][0]['title']
    
    if 'nl clinic' in company_found.lower():
        print(company_found)