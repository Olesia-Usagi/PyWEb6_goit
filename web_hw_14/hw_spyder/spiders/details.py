import scrapy
import re


class DetailsSpider(scrapy.Spider):
    name = 'details'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {'ITEM_PIPELINES': {'hw_spyder.pipelines.HwSpyderPipelineAuthor': 300}}

    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        full_name = extract_with_css('h3.author-title::text')
        born_d = " ".join(extract_with_css('.author-born-date::text').split()[:2])
        born_date = born_d.replace(',', '')
        born_year = "".join(extract_with_css('.author-born-date::text').split()[2])
        born_loc = extract_with_css('.author-born-location::text')
        born_location = re.sub(r'\bin\b', '', born_loc, flags=re.IGNORECASE)
        description = extract_with_css('.author-description::text')

        yield {
            'full_name': full_name,
            'born_date': born_date,
            'born_year': born_year,
            'born_location': born_location,
            'description': description
        }
