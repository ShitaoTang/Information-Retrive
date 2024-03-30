import os
import re
import requests
from bs4 import BeautifulSoup


header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
} 


class Crawler:
    start_url = "https://www.ietf.org/rfc/"

    def get_urls(self, rule):
        urls = rule.finditer(requests.get(self.start_url, headers = header).text)
        return urls

    def get_url(self, urls):
        for item in urls:
            url = self.start_url + item.groupdict()['name'] + ".txt"
            yield url

    def get_pages(self, url):
        try:
            res = requests.get(url, headers = header)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(res.text, 'html.parser')


def download_pages(crawler, rule, folder_path):
    '''
    Download web-pages from given URL obtained in crawler matching the regular expression 
    and save them to the specified foleder.

    Args:
    - crawler: Crawler instance used to fetch pages.
    - rule: Regular expression pattern for extracting URLs.
    - folder_path: Path to the folder where the pages will be saved.
    '''
    # get URL list
    urls = crawler.get_urls(rule = rule)
    # an iterator that yields URLs
    gen_url = crawler.get_url(urls = urls)

    for url in gen_url:
        bs = crawler.get_pages(url = url)
        # extract the direct filename from URL
        file_name = url.split("/")[-1]
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(bs.text)


# crawl English pages
folder_path_en = "downloaded/en"
rule_en = re.compile(r"<tr><td.*?href=\"(?P<name>.*?)\.txt\".*?</td></tr>")
os.makedirs(folder_path_en, exist_ok=True)
crawler_en = Crawler()
download_pages(crawler=crawler_en, rule=rule_en, folder_path=folder_path_en)
