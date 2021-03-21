import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        # print(response.status)
        # print(response.url)
        # response.xpath()
        # response.css()
        vacancy_link = response.xpath('//a[contains(@class, "icMQ_ _6AfZ9")]/@href'
                                      ).extract()
        for link in vacancy_link:
            page_link = 'https://www.superjob.ru' + link
            yield response.follow(page_link, callback=self.parse_vacancies)
        pass
        next_page = response.xpath(
            '//a[contains(@class, "icMQ_ bs_sM _3ze9n f-test-button-dalshe f-test-link-Dalshe")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def salary_check(self, salary):
        salary_max = 'null'
        salary_min = 'null'

        i = 0
        for item in salary:
            salary[i] = item.replace(u'\xa0', '')
            string = salary[i]
            if string != '' and string[0].isdigit() and string.isdigit() == False:
                salary[i] = string[:-4]
            i = i + 1

        if salary[0] == 'до':
            salary_max = salary[2]
        elif salary[0].isdigit():
            salary_min = salary[0]
            salary_max = salary[4]
        else:
            salary_min = salary[2]

        return salary_min, salary_max

    def parse_vacancies(self, response: HtmlResponse):
        title = response.xpath("//h1//text()").get()
        salary = response.xpath("//span[contains(@class, '_1OuF_ ZON4b')]//span/text()").getall()
        link = response.url
        web = 'superjob.ru'
        if len(salary) > 1:
            salary_output = self.salary_check(salary)
            salary_min = salary_output[0]
            salary_max = salary_output[1]
        else:
            salary_min = 'null'
            salary_max = 'null'
        yield JobparserItem(title=title, salary_min=salary_min, salary_max=salary_max, link=link, web=web)
