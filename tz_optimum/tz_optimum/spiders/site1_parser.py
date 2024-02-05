import scrapy
import json
import asyncio
import aiohttp

# Class for parsing www.scrapethissite.com/pages/ajax-javascript/ web page via api requests
class AdvanvedParser:
    # Initializing class instance and its attributes (output file path)
    def __init__(self) -> None:
        self.json_file = {}
        self.file_path = "result_1.json"

    # Function to get useful data for parsing 
    async def get_page_data(self, year):
        api_url = f"https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year={year}"
    
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return None
    
    # Function for retrieving only neccessary data from response and prettifying it
    def prettify_page_data(self, data : list) -> list:
        
        if len(data) == 0:
            return []
        
        result = []
        data = json.loads(data)
        
        for item in data:
            new_item = {
                "title" : item["title"].strip(),
                "nominations" : item["nominations"],
                "awards" : item["awards"],
                "best_picture" : True if "best_picture" in item else False
            }

            result.append(new_item)
        return result

    # Funtion to set_up and complement final json file
    def set_data(self, year, data : list):
        self.json_file[year] = data
    
    # Function to save resulting json file
    def generate_json(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.json_file, file, indent=2)

# Async function to parse asynchronously
async def process_task(year_string, parser):
    year = year_string.css('::text').get()

    # Some very hard data parsing
    response = await parser.get_page_data(year)

    response = parser.prettify_page_data(response)
    parser.set_data(year, response)

# Spider
class Site1ParserSpider(scrapy.Spider):
    name = "site1_parser"
    allowed_domains = ["www.scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/ajax-javascript/"]

    async def parse(self, response):
        self.log(f"Start parsing of {response.url}")
        base_url = response.url

        # Extract all existing year numbers 
        year_strings = response.css('.year-link')
        
        parser = AdvanvedParser()

        # ???
        tasks = [process_task(year_string, parser) for year_string in year_strings]

        await asyncio.gather(*tasks)
            
        # Finishing
        parser.generate_json()
        self.log("finishing parsing")