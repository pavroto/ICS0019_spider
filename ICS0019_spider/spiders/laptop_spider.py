import scrapy
import os


class LaptopCrawl(scrapy.Spider):
    name = "laptop"

    home_url = 'https://www.1a.ee'

    start_urls = [
        'https://www.1a.ee/c/arvutitehnika-burootarbed/sulearvutid-ja-tarvikud/sulearvutid/373'
    ]

    def parse(self, response, **kwargs):
        for block in response.css(
                "div.catalog-taxons-products-container div.catalog-taxons-products-container__grid-row div.catalog-taxons-product.catalog-taxons-product--grid-view"):
            page = scrapy.Request(
                os.path.join('https://www.1a.ee', block.css("a.catalog-taxons-product__name::attr(href)").get()[1:]),
                callback=self.parse_product)
            yield page

    def parse_product(self, response):
        def return_specifications(response):
            result = {}
            specifications_body = response.css("div.products-panel.universal-panel")

            for table in specifications_body.css("table.info-table"):
                for row in table.css("tr:not([class])"):
                    row_data = row.css("td")
                    if row_data[1].css("a.attribute-filter-link").get() is not None:
                        result[row_data[0].css("td::text").get()[1:-1]] = row_data[1].css(
                            "a.attribute-filter-link::text").get()
                    else:
                        result[row_data[0].css("td::text").get()[1:-1]] = row_data[1].css("td::text").get()[1:-1]

            return result

        result = {
            'name': response.css("h1::text").get()[1:-2],
            'price': response.css("span.price span::text").get(),
            'specifications': return_specifications(response)
        }

        yield result
