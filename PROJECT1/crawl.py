import os
import re
import requests
from bs4 import BeautifulSoup
from collections import deque
import threading

# pretend to be a browser and receive Chinese(simplified) pages
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9"
} 


class Crawler_en:
    '''
    A simple crawler that fetches web-pages from the IETF RFC index.

    Attributes:
    - start_url: The starting URL of the crawler.
    '''

    start_url = "https://www.ietf.org/rfc/"

    def get_urls(self, rule):
        '''find all URLs in the start_url page, return an iterator that yields URLs.'''
        urls = rule.finditer(requests.get(self.start_url, headers = header, verify = False).text)
        return urls

    def get_url(self, urls):
        '''concatenate prefix and filename to form a URL'''
        for item in urls:
            url = self.start_url + item.groupdict()['name'] + ".txt"
            yield url

    def get_pages(self, url):
        '''get html from given URL'''
        try:
            res = requests.get(url, headers = header, verify = False)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(res.text, 'html.parser')


def download_en_pages(crawler, rule, folder_path):
    '''
    Download webpages from given URL obtained in crawler matching the 
    regular expression and save them to the specified foleder.

    Args:
    - crawler: Crawler instance used to fetch pages.
    - rule: Regular expression pattern for extracting URLs.
    - folder_path: Path to the folder where the pages will be saved.
    '''

    # get URL list
    urls = crawler.get_urls(rule = rule)
    # an iterator that yields URLs
    gen_url = crawler.get_url(urls = urls)

    count = 0
    for url in gen_url:
        count += 1
        if count >= 600:
            break

        bs = crawler.get_pages(url = url)
        # extract the direct filename from URL
        file_name = url.split("/")[-1]
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
           file.write(bs.text)


def run_en_crawler():
    # crawl English pages
    folder_path_en = "downloaded/en"
    rule_en = re.compile(r"<tr><td.*?href=\"(?P<name>.*?)\.txt\".*?</td></tr>")
    os.makedirs(folder_path_en, exist_ok=True)
    crawler_en = Crawler_en()
    download_en_pages(crawler=crawler_en, rule=rule_en, folder_path=folder_path_en)


class Crawler_cn:
    '''
    A simple crawler that fetches webpages from the Chinese Wikipedia using BFS.

    Attributes:
    - start_url: The starting URL of the crawler.
    - add_urls: A set that stores all the URLs that have been added to the queue.
    - queue: A deque that stores the URLs that need to be fetched.
    - count: The number of pages that have been fetched.
    '''

    # start from searching "操作系统" in Chinese Wikipedia
    start_url = "https://zh.wikipedia.org/wiki/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F"
    add_urls = set()
    queue = deque([start_url])
    count = 0

    def download_cn_pages(self, rule, folder_path):
        '''
        Download web-pages from given URL obtained in crawler matching the
          regular expression and save them to the specified foleder.

        Args:
        - crawler: Crawler_en instance used to fetch pages.
        - rule: Regular expression pattern for extracting URLs.
        - folder_path: Path to the folder where the pages will be saved.
     '''

        while self.queue and self.count <= 600:
            cur_url = self.queue.pop()

            # unique URL 
            if cur_url in self.add_urls:
                continue
            else:
                self.add_urls.add(cur_url)
                self.count += 1
            
            try:
                res = requests.get(cur_url, headers = header, verify = False)
            except requests.exceptions.RequestException as e:
                print(f"\033[91m[Error]\033[0m Filed to get {cur_url}: {e}")

            res = requests.get(cur_url, headers = header, verify = False).text
            urls = rule.finditer(res)

            # extract the direct filename from URL
            file_name = requests.utils.unquote(cur_url.split("/")[-1])
            file_extension = ".txt"
            file_path = os.path.join(folder_path, file_name + file_extension)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(res)

            for url in urls:
                # concatenate prefix and filename to form a URL
                href = url.groupdict()['url']
                # only crawl Chinese pages
                if href.startswith('/wiki/%'):
                    self.queue.appendleft(f"https://zh.wikipedia.org{href}")


def run_cn_crawler():
    # crawl Chinese pages
    folder_path_cn = "downloaded/cn"
    rule_cn = re.compile(r"<a href=\"(?P<url>\/wiki\/(%[A-F0-9]{2})+)\" (title|class)")
    os.makedirs(folder_path_cn, exist_ok=True)
    crawler_cn = Crawler_cn()
    crawler_cn.download_cn_pages(rule=rule_cn, folder_path=folder_path_cn)

def main():
    thread1 = threading.Thread(target=run_en_crawler)
    thread2 = threading.Thread(target=run_cn_crawler)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
    
if __name__ == "__main__":
    main()