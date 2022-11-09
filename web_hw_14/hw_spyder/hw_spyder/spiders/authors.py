import scrapy
import re


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {'ITEM_PIPELINES': {'hw_spyder.pipelines.HwSpyderPipelineQuote': 300,
                                          'hw_spyder.pipelines.HwSpyderPipelineKeyword': 300,
                                          }
                       }

    def parse(self, response):
        base_url = 'http://quotes.toscrape.com'

        for quote in response.xpath("/html//div[@class='quote']"):
            author = quote.xpath("span/small/text()").get()
            new_quote = quote.xpath("span[@class='text']/text()").get()
            new_quote = re.sub(r'^“|"|”$', '', new_quote)
            new_keyword = quote.xpath("div[@class='tags']/a/text()").extract()
            # n_keyword = ', '.join(new_keyword)
            # n_about = quote.xpath("span/a/@href").get()
            # link_about = f"{base_url}{n_about}"

            yield {
                "author": author,
                "quote": new_quote,
                "keywords": new_keyword,
                # "about": link_about
            }

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
