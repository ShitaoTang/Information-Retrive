import os
import re
import requests
from bs4 import BeautifulSoup

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
} 

rule_en = re.compile(r"<tr><td.*?href=\"(?P<name>.*?)\.txt\".*?</td></tr>")

class Crawler:
    start_url = "https://www.ietf.org/rfc/"

    def get_urls(self, rule):
        urls = rule.finditer(requests.get(self.start_url, headers = header).text)
        return urls

    def get_url(self, urls):
        for item in urls:
            url = self.start_url + item.groupdict()['name'] + ".txt"
            yield url

    def get_text(self, url):
        try:
            res = requests.get(url, headers = header)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(res.text, 'html.parser')

folder_path = "downloaded/en"
os.makedirs(folder_path, exist_ok=True)

crawler = Crawler()
_urls = crawler.get_urls(rule = rule_en)
# for _ in range(0, 500):
#     _url = crawler.get_url(urls = _urls)
#     _url =  
#     text = crawler.get_text(url = _url)
#     file_path = os.path.join(folder_path, f"webpage_{_+1}.txt")
#     with open(file_path, "w", encoding="utf-8") as file:
#         file.write(text)
_ = 0
for item in _urls:
    url = crawler.start_url + item.groupdict()['name'] + ".txt"
    res = requests.get(url)
    _ += 1
    file_path = os.path.join(folder_path, f"webpage_{_+1}.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(res.text)
    if _ >= 10:
        break