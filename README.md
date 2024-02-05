# Scrapy-Parser for OptimumPrice

## This repository contains a Scrapy-based web scraping project developed for the OptimumPrice test task. The scraper is designed to extract data from the websites https://www.scrapethissite.com/pages/ajax-javascript/ and https://www.scrapethissite.com/pages/forms/

## Features:
Scrapy Framework: Utilizes the Scrapy framework for efficient and modular web scraping.
aiohttp and asyncio Integration: Incorporates aiohttp and asyncio to handle asynchronous requests, enhancing performance and speed.

## All parsing results are presented in JSON-files named result_1.json and result_2.json respectively

## Instructions:
1. Clone repository
```bash
git clone https://github.com/Amir23714/optimumprice_tz.git
```

2. Navigate to the project folder
```bash
cd tz_optimum
```

3. Install requirements
```bash
pip install requirements.txt
```

4. To run first website parser use:
```bash
scrapy crawl site1_parser
```

5. To run second website parser use:
```bash
scrapy crawl site2_parser
```
