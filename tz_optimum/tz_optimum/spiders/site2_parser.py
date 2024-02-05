import scrapy
import json

# Class for json file generating and updating
class JsonManager:
    def __init__(self) -> None:
        self.json_file = []
        self.file_path = "result_2.json"
    
    def set_data(self, name, year, wins, losses, ot_losses, win_rate, goals_for, goals_againts, rate):
        
        new_team = {
            "team_name" : name,
            "year" : year,
            "wins" : wins,
            "losses" : losses,
            "OT_losses" : ot_losses,
            "win_rate" : win_rate,
            "goals_for" : goals_for,
            "goals_againts" : goals_againts,
            "+/-" : rate
        }

        self.json_file.append(new_team)
    
    def generate_json(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.json_file, file, indent=2)

# Spider
class Site2ParserSpider(scrapy.Spider):
    name = "site2_parser"
    allowed_domains = ["www.scrapethissite.com"]
    start_urls = ["https://www.scrapethissite.com/pages/forms/"]

    def parse(self, response):
        self.log(f"Start parsing of {response.url}")
        self.json_manager = JsonManager()
        
        # Flag for skipping first page due to the peculiarities of the site structure
        self.first_page_flag = True

        # Queries to send requests. Can be extended for many other ones
        queries : list = ["New York"]

        for query in queries:
            form_data = {
                'q': query,
            }

            yield scrapy.FormRequest.from_response(
                response,
                formdata=form_data,
                callback=self.parse_query
            )

    def parse_query(self, response):
        base_url = "https://www.scrapethissite.com"
        teams = response.css("tr.team")

        if not self.first_page_flag:
            for team in teams:
                name = team.css('.name').css('::text').get()
                name = name.strip() if name else "N/A"

                year = team.css(".year").css('::text').get()
                year = year.strip() if year else "N/A"

                wins = team.css(".wins").css('::text').get()
                wins = wins.strip() if wins else "N/A"

                losses = team.css(".wins").css('::text').get()
                losses = losses.strip() if losses else "N/A"

                ot_losses = team.css(".ot-losses").css('::text').get()
                ot_losses = ot_losses.strip() if ot_losses else "N/A"
                ot_losses = "N/A" if ot_losses == "" else ot_losses

                win_rate = team.css(".pct").css('::text').get()
                win_rate = win_rate.strip() if win_rate else "N/A"

                gf = team.css(".gf").css('::text').get()
                gf = gf.strip() if gf else "N/A"

                ga = team.css(".ga").css('::text').get()
                ga = ga.strip() if ga else "N/A"

                rate = team.css(".diff").css('::text').get()
                rate = rate.strip() if rate else "N/A"

                self.json_manager.set_data(name, year, wins, losses, ot_losses, win_rate, gf, ga, rate)
        
        else:
            self.first_page_flag = False
        
        # Pagination
        next_page = response.css('ul.pagination li a[aria-label="Next"]')

        # If there is no remaining pages - finish
        if not next_page:
            self.json_manager.generate_json()
            self.log("finishing!!!")
            return
        
        # Otherwise - extract next page link and continue
        next_page_prelink = next_page.attrib['href']
        next_page_link = f"{base_url}{next_page_prelink}"

        yield scrapy.Request(next_page_link, callback=self.parse_query, meta=response.meta)