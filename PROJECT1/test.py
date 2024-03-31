# import requests
# import re

# start_url = "https://www.ietf.org/rfc/"
# res = requests.get(start_url).text

# rule_en = re.compile(r"<tr><td.*?href=\"(?P<name>.*?)\.txt\".*?</td></tr>")
# urls = rule_en.finditer(res)

# for item in urls:
#     r = item.groupdict()
#     print(r['name'])

import re
import requests
import os
from bs4 import BeautifulSoup
from collections import deque

def get_links(starturl):
    added_urls = set() 
    queue = deque([starturl])
    count = 0

    while queue and count <= 600:
        cur_url = queue.pop()

        if cur_url in added_urls:
            continue
        else:
            print(f"\033[92m[Success]\033[0m {cur_url}")
            added_urls.add(cur_url)
            count += 1

        try:
            res = requests.get(cur_url)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"\033[91m[Error]\033[0m Filed to get {cur_url}: {e}")

        res = requests.get(cur_url).text
        rule = re.compile(r"<a href=\"(?P<url>\/wiki\/(%[A-F0-9]{2})+)\" (title|class)")
        urls = rule.finditer(res)

        for url in urls:
            href = url.groupdict()['url']
            if href.startswith('/wiki/%'):
                queue.appendleft(f"https://zh.wikipedia.org{href}")


    return added_urls

start_url = "https://zh.wikipedia.org/wiki/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F"
addedurls = get_links(start_url)
print(len(addedurls))