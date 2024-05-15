import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
import time

class AirbnbspiderSpider(scrapy.Spider):
    name = "airbnbspider"
    allowed_domains = ["airbnb.com.br"]
    start_urls = ["https://www.airbnb.com.br/s/madrid/experiences"]

    def __init__(self, *args, **kwargs):
        super(AirbnbspiderSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome()  # ou webdriver.Firefox(), webdriver.Edge(), etc.

    def parse(self, response):
        self.driver.get(response.url)

        click_count = 0
        while True:
            try:
                show_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Mostrar mais")]'))
                )
                show_more_button.click()
                time.sleep(2)  # Espere um pouco para o conteúdo carregar
                click_count += 1
                self.log(f'Clicou em "Mostrar mais" {click_count} vezes')
            except:
                self.log('Botão "Mostrar mais" não encontrado ou não clicável')
                break

        page_source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=page_source, encoding='utf-8')

        # Seleciona todos os elementos de produtos com as classes 'fjicacb' ou 'chpsl5'
        products = response.xpath('//div[contains(@class, "fjicacb") or contains(@class, "chpsl5")]')
        self.log(f'Número total de produtos encontrados: {len(products)}')
        seen = set()

        for product in products:
            aria_label = product.xpath('.//a[@aria-label]/@aria-label').get()
            href = product.xpath('.//a[@aria-label]/@href').get()
            price = product.xpath('.//span[contains(@class, "_1y74zjx")]/text()').get()
            duration = product.xpath('.//span[contains(@class, "k4fuxou")]/text()').get()
            score = product.xpath('.//span[contains(text(), "Pontuação média")]/text()').get()

            if href not in seen:
                seen.add(href)
                self.log(f'aria-label: {aria_label}')
                self.log(f'href: {href}')
                self.log(f'price: {price}')
                self.log(f'duration: {duration}')
                self.log(f'score: {score}')

                yield {
                    'aria_label': aria_label,
                    'href': href,
                    'price': price,
                    'duration': duration,
                    'score': score
                }

    def closed(self, reason):
        self.driver.quit()
