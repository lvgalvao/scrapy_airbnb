import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from airbnbscraper.items import AirbnbscraperItem
import time

class AirbnbspiderSpider(scrapy.Spider):
    """
    Spider para coletar dados de experiências listadas no AirBnB em Madrid.

    O spider clica no botão "Mostrar mais" até que todos os produtos estejam carregados,
    e então coleta informações sobre cada experiência, incluindo título, link, preço,
    duração e pontuação média.
    """
    name = "airbnbspider"
    allowed_domains = ["airbnb.com.br"]
    start_urls = ["https://www.airbnb.com.br/s/madrid/experiences"]

    custom_settings = {
        'FEEDS': {
        'resultados.json': {'format': 'json', 'overwrite': True},
        }
    }
    
    def __init__(self, *args, **kwargs):
        """
        Inicializa o spider e o WebDriver.

        Args:
            *args: Argumentos posicionais.
            **kwargs: Argumentos nomeados.
        """
        super(AirbnbspiderSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome()  # ou webdriver.Firefox(), webdriver.Edge(), etc.

    def parse(self, response):
        """
        Método principal de parsing.

        Este método navega até a URL inicial, clica no botão "Mostrar mais" até que
        todos os produtos estejam carregados, e então coleta os dados dos produtos.

        Args:
            response (HtmlResponse): A resposta inicial da página.

        Yields:
            AirbnbscraperItem: Um item contendo os dados extraídos de cada produto.
        """
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
        seen = set()

        for product in products:
            aria_label = product.xpath('.//a[@aria-label]/@aria-label').get()
            href = product.xpath('.//a[@aria-label]/@href').get()
            price = product.xpath('.//span[contains(@class, "_1y74zjx")]/text()').get()
            duration = product.xpath('.//span[contains(@class, "k4fuxou")]/text()').get()
            score = product.xpath('.//span[contains(text(), "Pontuação média")]/text()').get()

            if href not in seen:
                seen.add(href)

                airbnb_item = AirbnbscraperItem()
                airbnb_item['aria_label'] = aria_label
                airbnb_item['href'] = href
                airbnb_item['price'] = price
                airbnb_item['duration'] = duration
                airbnb_item['score'] = score

                yield airbnb_item

    def closed(self, reason):
        """
        Método chamado quando o spider é fechado.

        Args:
            reason (str): A razão pela qual o spider foi fechado.
        """
        self.driver.quit()
