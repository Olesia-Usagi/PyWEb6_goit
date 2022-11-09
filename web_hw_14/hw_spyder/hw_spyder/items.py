import scrapy


class QuoteItem(scrapy.Item):
    # auther = scrapy.Field()
    quote = scrapy.Field()
    # about = scrapy.Field()


class KeywordItem(scrapy.Item):
    key_word = scrapy.Field()


class AuthorItem(scrapy.Item):
    full_name = scrapy.Field()
    born_date = scrapy.Field()
    born_year = scrapy.Field()
    born_location = scrapy.Field()
    description = scrapy.Field()