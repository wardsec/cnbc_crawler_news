# Crawler CNBC

Este Crawler permite que você retire notícias relacionados a palavra que você quiser dentro de um intervalo de datas especificado.
Este Projeto faz parte de um outro Projeto Privado que tem a afinidade de usar NLP para tomada de decisão de compra de crypto ativos.

## Pré-requisitos

- Python 3.x ma.
- Biblioteca Selenium instalada (`pip install selenium==4.2.0`).
- WebDriver do Edge instalado e seu caminho especificado corretamente no script.
- Biblioteca Dateutil instalada (`pip install python-dateutil`).

## Uso

1. Clone ou baixe este repositório para sua máquina local.
2. Navegue até o diretório que contém o script.
3. Execute o script executando o comando `python cnbc_scraper.py`.
4. Siga as instruções para inserir a data de início e a data de término no formato `aaaa-mm-dd`.
5. O script irá buscar a CNBC em busca de artigos contendo a palavra-chave "Bitcoin" (ou a palavra que desejar) dentro do intervalo de datas especificado e salvar os resultados em um arquivo CSV chamado `CNBC_articles.csv` no mesmo diretório.

## Customização

- Você pode modificar a função `contains_bitcoin_keywords()` para alterar as palavras-chave usadas para filtrar os artigos.
- Ajuste os valores de tempo de espera no método `scrape_articles()` conforme necessário.

## Notas

- Este script depende de técnicas de crawling e pode estar sujeito a alterações na estrutura do site da CNBC.
- Use com responsabilidade e esteja ciente dos termos de serviço da CNBC e de quaisquer restrições legais.

