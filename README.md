# AirBnB Scraper

Este projeto utiliza Scrapy e Selenium para coletar dados de experiências listadas no AirBnB em Madrid. O spider clica no botão "Mostrar mais" até que todos os produtos estejam carregados, e então coleta informações sobre cada experiência, incluindo título, link, preço, duração e pontuação média.

## Requisitos

- Python 3.12.1
- Scrapy
- Selenium
- Webdriver do Chrome (ou outro navegador de sua escolha)

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/airbnb-experience-scraper.git
    cd airbnb-experience-scraper
    ```

2. Crie um ambiente virtual e instale as dependências:

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    pip install scrapy selenium
    ```

3. Certifique-se de ter o WebDriver do Chrome (ou outro navegador) instalado e configurado no PATH.

## Configuração do Projeto

Configure o arquivo `settings.py` para salvar os logs em um arquivo:

```python
# settings.py

LOG_ENABLED = True
LOG_LEVEL = 'INFO'
LOG_FILE = 'scrapy_log.txt'
```

## Executando o Spider

Para executar o spider e salvar os resultados em um arquivo JSON:

```bash
scrapy crawl airbnbspider -o resultados.json
```

## Estrutura do Projeto

```
airbnb-experience-scraper/
│
├── myproject/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders/
│       ├── __init__.py
│       └── airbnbspider.py
├── scrapy.cfg
└── README.md
```

## Fluxo de Execução

```mermaid
graph TD;
    A[Iniciar Scrapy] --> B[Inicializar WebDriver]
    B --> C[Navegar para a URL de Início]
    C --> D{Botão "Mostrar mais" Disponível?}
    D -- Sim --> E[Clicar no Botão "Mostrar mais"]
    E --> F[Aguardar Carregamento]
    F --> D
    D -- Não --> G[Capturar HTML Atualizado]
    G --> H[Extrair Dados dos Produtos]
    H --> I[Salvar Dados Extraídos]
    I --> J[Fechar WebDriver]
```