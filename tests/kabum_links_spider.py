import scrapy


def first(sel, xpath):
    return sel.xpath(xpath).extract_first()


class KabumNotebooklLister(scrapy.Spider):
    name='Spider_Kabum'
    start_urls = ['http://www.kabum.com.br/computadores/notebooks-ultrabooks']

    def parse(self, response):
        for box_page in response.css(".listagem-box"):
            yield {
                'link': box_page.css('.listagem-titulo_descr a::attr(href)').extract_first(),
                'description': box_page.css('.listagem-titulo_descr a::text').extract_first(),
            }

        link_next = response.xpath('//*[@id="BlocoConteudo"]/div[2]/div/div[33]/form/table//tr/td[7]/a/@href').extract_first()

        if link_next:
            yield scrapy.Request('http://www.kabum.com.br/computadores/notebooks-ultrabooks%s'%link_next)

