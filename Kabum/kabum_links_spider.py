import scrapy


def first(sel, xpath):
    return sel.xpath(xpath).extract_first()


class KabumNotebooklLister(scrapy.Spider):
    name='Spider_Kabum'
    start_urls = ['http://www.kabum.com.br/computadores/notebooks-ultrabooks']

    def parse(self, response):
        for box_page in response.xpath('//*[@id="BlocoConteudo"]/div[2]/div/div[@class="listagem-box"]/div[@class="listagem-titulo_descr"]/span[@class="H-titulo"]/a[(contains(@href, "/notebook-")) or (contains(@href, "/ultrabook-"))]'):   
            link = box_page.xpath('./@href').extract()
            description = box_page.xpath('normalize-space(./text())').extract_first()
            yield dict(link=link, description=description)

        link_next = response.xpath('//*[@id="BlocoConteudo"]/div[2]/div/div[33]/form/table//tr/td[7]/a/@href').extract_first()

        if link_next:
            yield scrapy.Request('http://www.kabum.com.br/computadores/notebooks-ultrabooks%s'%link_next)