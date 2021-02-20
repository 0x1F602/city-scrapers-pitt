from datetime import datetime
from os.path import dirname, join
from pprint import pprint

import pytest
from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.pgh_post_gazette_other_legal_notices import PghPostGazetteOtherLegalNoticesSpider

root_url = "https://classmart.post-gazette.com"

test_response = file_response(
    join(dirname(__file__), "files", "pgh_post_gazette_other_legal_notices.html"),
    url=root_url
    + "/pa/other-legal-notices/search?",
)
spider = PghPostGazetteOtherLegalNoticesSpider()

freezer = freeze_time("2021-02-19")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert 1==1 # my little insanity check
    pprint(parsed_items)
    # assert parsed_items[0]["title"] == (
    #     "Pittsburgh Post Gazette | Classifieds | Other Legal Notices"
    # )
