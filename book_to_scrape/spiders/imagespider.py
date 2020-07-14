# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader
from book_to_scrape.items import BookToScrapeItem


class ImagesToScrapeSpider(scrapy.Spider):
    name = 'downloader'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for article in response.xpath("//article[@class='product_pod']"):
            loader = ItemLoader(item = BookToScrapeItem(), selector=article)
            relative_url = article.xpath(".//div[@class='image_container']/a/img/@src").extract_first()
            absolute_url = response.urljoin(relative_url)
            loader.add_value('image_urls', absolute_url)
            loader.add_xpath('book_name','.//h3/a/@title')
            yield loader.load_item()
        next_page = response.xpath("//section/div[2]/div/ul/li[@class = 'next']/a/@href").get()
        absolute_next_page = response.urljoin(next_page)

        if absolute_next_page:
            yield scrapy.Request(url=absolute_next_page,callback=self.parse)