import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=Python']

    def parse(self, response: HtmlResponse):
        # print(response.status)
        # print(response.url)
        # response.xpath()
        # response.css()
        vacancy_link = response.xpath('//div[contains(@class, "vacancy-serp-item")]//a[contains(@class, "HH-LinkModifier")]/@href'
                                      ).extract()
        for link in vacancy_link:
            yield response.follow(link, callback=self.parse_vacancies)
        pass
        next_page = response.xpath('//a[contains(@class, "-Pager-Controls-Next")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def salary_check(self, salary):
        salary_max = 'null'
        salary_min = 'null'
        i = 0
        for item in salary:
            salary[i] = item.replace(u'\xa0', '')
            i = i + 1

        if salary[3].isdigit():
            salary_max = salary[3]
        else:
            salary_max = 'null'

        if salary[1].isdigit() and salary[0] == 'от ':
            salary_min = salary[1]
        elif salary[1].isdigit() and salary[0] == 'до ':
            salary_max = salary[1]
        else:
            salary_min = 'null'
            salary_max = 'null'
        return salary_min, salary_max


    def link_end(self, link):
        new_link = link[:link.rfind("?")]
        return new_link

    def parse_vacancies(self, response: HtmlResponse):
        title = response.xpath("//h1//text()").get()
        salary = response.xpath("//p[contains(@class, 'vacancy-salary')]//span/text()").getall()
        link = self.link_end(response.url)
        web = 'hh.ru'
        if len(salary) > 1:
            salary_output = self.salary_check(salary)
            salary_min = salary_output[0]
            salary_max = salary_output[1]
        else:
            salary_min = 'null'
            salary_max = 'null'
        yield JobparserItem(title=title, salary_min=salary_min, salary_max=salary_max, link=link, web=web)
