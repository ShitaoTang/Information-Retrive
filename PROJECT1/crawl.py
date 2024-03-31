import os
import re
import requests
from bs4 import BeautifulSoup
from collections import deque
import threading
import smtplib
from email.mime.text import MIMEText
from email.header import Header

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
} 


class Crawler_en:
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


def download_en_pages(crawler, rule, folder_path):
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

    # start_url = "https://zh.wikipedia.org/wiki/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F"

    # start_url = "https://zh.wikipedia.org/wiki/%E6%90%9C%E7%B4%A2%E5%BC%95%E6%93%8E"

    start_url = "https://zh.wikipedia.org/wiki/%E9%83%B4%E5%B7%9E%E5%B8%82"

    add_urls = set()
    queue = deque([start_url])
    count = 0

    def download_cn_pages(self, rule, folder_path):
        '''
        Download web-pages from given URL obtained in crawler matching the regular expression 
        and save them to the specified foleder.

        Args:
        - crawler: Crawler_en instance used to fetch pages.
        - rule: Regular expression pattern for extracting URLs.
        - folder_path: Path to the folder where the pages will be saved.
    '''

        while self.queue and self.count <= 600:
            cur_url = self.queue.pop()

            if cur_url in self.add_urls:
                continue
            else:
                print(f"\033[92m[Success]\033[0m {cur_url}")
                self.add_urls.add(cur_url)
                self.count += 1
            
            try:
                res = requests.get(cur_url, headers = header, verify = False)
                res.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"\033[91m[Error]\033[0m Filed to get {cur_url}: {e}")

            res = requests.get(cur_url, headers = header, verify = False).text
            urls = rule.finditer(res)

            file_name = requests.utils.unquote(cur_url.split("/")[-1])
            file_extension = ".txt"
            file_path = os.path.join(folder_path, file_name + file_extension)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(res)

            for url in urls:
                href = url.groupdict()['url']
                if href.startswith('/wiki/%'):
                    self.queue.appendleft(f"https://zh.wikipedia.org{href}")


def run_cn_crawler():
    # crawl Chinese pages
    folder_path_cn = "downloaded/cn"
    rule_cn = re.compile(r"<a href=\"(?P<url>\/wiki\/(%[A-F0-9]{2})+)\" (title|class)")
    os.makedirs(folder_path_cn, exist_ok=True)
    crawler_cn = Crawler_cn()
    crawler_cn.download_cn_pages(rule=rule_cn, folder_path=folder_path_cn)


def send_email():
    sender = '744317484@qq.com'  
    receivers = ['tst17@my.swjtu.edu.cn']  
    # auth_code = ""  

    message = MIMEText('webpages download successfully!', 'plain', 'utf-8')
    message['From'] = Header("Sender<%s>" % sender) 
    message['To'] = Header("Receiver<%s>" % receivers[0])  

    subject = 'Webpages Downloaded Successfully!'
    message['Subject'] = Header(subject, 'utf-8')


    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(sender, auth_code)
        server.sendmail(sender, receivers, message.as_string())
        print("\033[92m[Success]\033[0m Email sent successfully!")
        server.close()
    except smtplib.SMTPException:
        print("\033[91m[Error]\033[0m Failed to send email!")


# if __name__ == "__main__":
#     thread1 = threading.Thread(target=run_en_crawler)
#     thread2 = threading.Thread(target=run_cn_crawler)

#     thread1.start()
#     thread2.start()

#     thread1.join()
#     thread2.join()
    
#     send_email()


run_cn_crawler()
send_email()