import re
from datetime import datetime

from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider

# Just for my own debugging purposes
from pprint import pprint

BASE_URL = "https://classmart.post-gazette.com"
TITLE = "Pittsburgh Post Gazette | Classifieds | Other Legal Notices"

class PghPostGazetteOtherLegalNoticesSpider(CityScrapersSpider):
    name = "pgh_post_gazette_other_legal_notices"
    agency = "TODO CHANGEME DONOTPASS"
    timezone = "America/New_York"
    start_urls = [BASE_URL + "/pa/other-legal-notices/search?"]

    def parse(self, response):
        probably_notices = (
            # response.xpath('/html/body/main/div[1]/div[2]/section[2]/div[5]/div[1]/div[1]/div/div')
            response.xpath('/html/body/main/div[1]/div[2]/section[2]/div[5]/div[1]/div')
            #.getall() # This flattens it into a giant text, we dun want that
        )

        title = "Unknown"
        index = 0
        for unknown in probably_notices:
            title = unknown.xpath('.//span[@class="title-text"]/text()').get()
            linky_selector_list = unknown.xpath('.//span[@class="post-link"]/a')
            preview_description = unknown.xpath('.//div[@class="post-summary-description"]/span[@class="post-copy"]/text()').getall()
            preview_description = ' '.join(preview_description)
            links = []
            for linky_node in linky_selector_list:
                pprint(BASE_URL + linky_node.attrib['href'])
            # pprint(unknown.get())
            print("INDEX " + str(index))
            pprint(title)
            pprint(preview_description)
            index+=1

        # print("Testing testing testing stdout")
        # pprint(probably_notices)

        meeting = Meeting(
            title="Placeholder",
            description="Placeholder",
            classification="Placeholder",
            start="Placeholder",
            end="Placeholder",
            all_day="Placeholder",
            time_notes="Placeholder",
            location="Placeholder",
            links="Placeholder",
            source="Placeholder",
        )

        yield meeting
