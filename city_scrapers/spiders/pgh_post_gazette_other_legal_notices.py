import re
from datetime import datetime
from urllib.parse import urljoin

import scrapy
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
    start_urls = [urljoin(BASE_URL, "/pa/other-legal-notices/search?")]

    relevancy_threshold = 2
    def _is_this_relevant(self, text):
        is_relevant = 0
        CONTAINS_MEETING = re.compile(r"meeting", re.IGNORECASE)
        CONTAINS_LEGALESE = re.compile(r"(Notice is hereby given)|(Pursuant to the Sunshine Act)", re.IGNORECASE)
        if CONTAINS_MEETING.search(text):
            is_relevant += 1
        if CONTAINS_LEGALESE.search(text):
            is_relevant += 1
        return is_relevant

    def parse_view_details_page(self, response):
        title = (
            response.xpath('.//h1[@class="details-ad-title"]/text()')
        )
        more_deets = (
            response.xpath('.//div[@class="details-ad-body"]/text()')
        )
        # print("more_deets")
        # pprint(more_deets.getall())

        body_text = "".join(more_deets.getall())

        how_relevant = self._is_this_relevant(body_text)
        if how_relevant < self.relevancy_threshold:
            return

        meeting = Meeting(
            title=title.get(),
            description=body_text,
            # start=datetime.now(),
            start=self._parse_start(response),
            end=None,
            location=self._parse_location(response),
            source=response.url,
        )

        meeting["status"] = self._get_status(meeting)
        meeting["id"] = self._get_id(meeting)

        yield meeting

    def _parse_start(self, response):
        return datetime.now()

    def _parse_location(self, response):
        return {
            "name":"Narnia",
            "address":"1313 Dead End Lane"
        }

    def parse(self, response):
        probably_notices = (
            # response.xpath('/html/body/main/div[1]/div[2]/section[2]/div[5]/div[1]/div[1]/div/div')
            response.xpath('/html/body/main/div[1]/div[2]/section[2]/div[5]/div[1]/div')
            #.getall() # This flattens it into a giant text, we dun want that
        )

        # Our next moves
        requests = []

        title = "Unknown"
        index = 0
        for unknown in probably_notices:
            title = unknown.xpath('.//span[@class="title-text"]/text()').get()
            linky_selector_list = unknown.xpath('.//span[@class="post-link"]/a')
            preview_description = unknown.xpath('.//div[@class="post-summary-description"]/span[@class="post-copy"]/text()').getall()
            preview_description = ' '.join(preview_description)
            for linky_node in linky_selector_list:
                pprint(BASE_URL + linky_node.attrib['href'])
                followup_request = scrapy.Request(urljoin(BASE_URL,linky_node.attrib['href']), callback=self.parse_view_details_page)
                yield followup_request
                
            # pprint(unknown.get())
            # print("INDEX " + str(index))
            # pprint(title)
            # pprint(preview_description)
            # index+=1

        # print("Testing testing testing stdout")
        # pprint(probably_notices)

        # meeting = Meeting(
        #     title="Placeholder",
        #     description="Placeholder",
        #     classification="Placeholder",
        #     start="Placeholder",
        #     end="Placeholder",
        #     all_day="Placeholder",
        #     time_notes="Placeholder",
        #     location="Placeholder",
        #     links="Placeholder",
        #     source="Placeholder",
        # )
        # yield requests 
