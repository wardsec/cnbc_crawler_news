import csv
import re
import time

from dateutil.parser import parse
from selenium import webdriver

edge_driver_path =r""


# Function to write data to a CSV file
def write_output(data, file_name):
    print('Escrevendo CSV...')
    keys = data[0].keys()
    with open(file_name, 'a+', encoding='utf-8', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print('CSV gerado.')

# Function to check if the given string contains any keywords related to Bitcoin
def contains_bitcoin_keywords(text):
    return re.search(r'\bbitcoin\b', text, re.IGNORECASE) is not None

# Class to scrape news articles from CNBC
class CNBCScraper:
    def __init__(self, start_date, end_date):
        self.search_term = 'Bitcoin'
        self.start_date = parse(start_date)
        self.end_date = parse(end_date)
        self.links = []

    # Check if the given date is within the specified range
    def is_within_date_range(self, date):
        page_date = parse(date)
        return self.start_date <= page_date <= self.end_date

    # Scrapes news articles from CNBC
    def scrape_articles(self, sleep_time=3):
        print('Scraping...')
        links = {}
        days = (self.end_date.date() - self.start_date.date()).days + 1

        driver = webdriver.Edge(executable_path=edge_driver_path)
        driver.get('http://search.cnbc.com/rs/search/view.html?partnerId=2000'
                   + f'&keywords={self.search_term}'
                   + f'&sort=date&type=news&source=CNBC.com'
                   + f'&pubtime={days}&pubfreq=d')

        time.sleep(15)

        select_element = driver.find_element_by_xpath('//select[@class="minimal SearchResults-searchResultsSelect"]')
        select_element.find_element_by_xpath(".//option[contains(text(), 'Articles')]").click()
        time.sleep(sleep_time)

        for _ in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"
                                  "var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            time.sleep(2)

        results = driver.find_elements_by_xpath('//div[@class="SearchResult-searchResult SearchResult-standardVariant"]')

        articles_data = []

        for result in results:
            try:
                pub_date = result.find_element_by_xpath(".//span[@class='SearchResult-publishedDate']").text
                title = result.find_element_by_xpath('.//span[@class="Card-title"]').text
                link = result.find_element_by_xpath('.//a[@class="resultlink"]').get_attribute('href')

                if contains_bitcoin_keywords(title) and link not in links and self.is_within_date_range(pub_date):
                    links[link] = True
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(link)
                    time.sleep(10)

                    article_text = ''
                    for para in driver.find_elements_by_xpath('//div[@class="group"]'):
                        for element in para.find_elements_by_xpath('.//p'):
                            article_text += element.text

                    article_data = {
                        'title': title,
                        'date_published': pub_date,
                        'article_link': link,
                        'text': article_text
                    }
                    articles_data.append(article_data)
                    time.sleep(sleep_time)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
            except Exception as e:
                print(f"An error occurred: {e}")

        self.links = links
        return articles_data

# Main function to run the scraper
def run_scraper(start_date, end_date):
    scraper = CNBCScraper(start_date, end_date)
    articles_data = scraper.scrape_articles()
    if len(articles_data) == 0:
        print('Nenhuma noticia encontrada com as keywords especificadas no intervalo de tempo especificado.')
        
    else:
        write_output(articles_data, 'CNBC_articles.csv')

if __name__ == "__main__":
    start_date = input('Data de inicio (yyyy-mm-dd): ')
    end_date = input('Data de fim (yyyy-mm-dd): ')
    run_scraper(start_date, end_date)
