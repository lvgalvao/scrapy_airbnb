# AirBnB Experience Scraper Documentation

Bem-vindo à documentação do AirBnB Experience Scraper. Este projeto utiliza Scrapy e Selenium para coletar dados de experiências listadas no AirBnB em Madrid. O spider clica no botão "Mostrar mais" até que todos os produtos estejam carregados, e então coleta informações sobre cada experiência, incluindo título, link, preço, duração e pontuação média.

## Visão Geral

Este projeto foi desenvolvido para automatizar a coleta de dados de experiências no AirBnB, permitindo que você obtenha informações detalhadas sobre cada experiência disponível em Madrid.

### Funcionalidades

- Coleta automática de dados de experiências.
- Extração de título, link, preço, duração e pontuação média de cada experiência.
- Navegação automática e carregamento dinâmico de mais produtos.
- Geração de logs detalhados para depuração e monitoramento.

## Comandos do Projeto

Aqui estão alguns comandos úteis para gerenciar e executar o projeto:

* `mkdocs serve` - Inicie o servidor de documentação com recarregamento automático.
* `mkdocs build` - Construa o site de documentação estática.
* `scrapy crawl airbnbspider` - Execute o spider para coletar dados das experiências.

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```plaintext
airbnb-experience-scraper/
│
├── airbnbscraper/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders/
│       ├── __init__.py
│       └── airbnbspider.py
├── docs/
│   ├── index.md
│   └── spider.md
├── mkdocs.yml
└── scrapy.cfg
```