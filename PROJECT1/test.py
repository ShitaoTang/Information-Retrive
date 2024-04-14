# # import requests
# # import re

# # start_url = "https://www.ietf.org/rfc/"
# # res = requests.get(start_url).text

# # rule_en = re.compile(r"<tr><td.*?href=\"(?P<name>.*?)\.txt\".*?</td></tr>")
# # urls = rule_en.finditer(res)

# # for item in urls:
# #     r = item.groupdict()
# #     print(r['name'])

# import winsound
# import time
# import re
# import requests
# import os
# from bs4 import BeautifulSoup
# from collections import deque


# header = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
# } 


# def get_links(starturl):
#     added_urls = set() 
#     queue = deque([starturl])
#     count = 0

#     while queue and count <= 100:
#         cur_url = queue.pop()

#         if cur_url in added_urls:
#             continue
#         else:
#             print(f"\033[92m[Success]\033[0m {cur_url}")
#             added_urls.add(cur_url)
#             count += 1

#         try:
#             res = requests.get(cur_url, headers = header, verify = False)
#             res.raise_for_status()
#         except requests.exceptions.RequestException as e:
#             print(f"\033[91m[Error]\033[0m Filed to get {cur_url}: {e}")

#         res = requests.get(cur_url, headers = header, verify = False).text
#         rule = re.compile(r"<a href=\"(?P<url>\/wiki\/(%[A-F0-9]{2})+)\" (title|class)")
#         urls = rule.finditer(res)

#         for url in urls:
#             href = url.groupdict()['url']
#             if href.startswith('/wiki/%'):
#                 queue.appendleft(f"https://zh.wikipedia.org{href}")


#     return added_urls

# start_url = "https://zh.wikipedia.org/wiki/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F"
# addedurls = get_links(start_url)
# print(len(addedurls))

# def beep(duration):
#     winsound.Beep(440, duration)

# duration = 10000
# print("Completed!")
# beep(duration)
   

# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header


# sender = 'xxxxxxxxxxxx@xx.com'  
# receivers = ['tst17@my.swjtu.edu.cn']  
# # auth_code = "xxxxxxxx"

# message = MIMEText('Python send email', 'plain', 'utf-8')
# message['From'] = Header("Sender<%s>" % sender) 
# message['To'] = Header("Receiver<%s>" % receivers[0]) 

# subject = 'Python SMTP test'
# message['Subject'] = Header(subject, 'utf-8')


# try:
#     server = smtplib.SMTP_SSL('smtp.qq.com', 465)
#     server.login(sender, auth_code)
#     server.sendmail(sender, receivers, message.as_string())
#     print("[SUCCESS]")
#     server.close()
# except smtplib.SMTPException:
#     print("[FAILED]")

# import requests

# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
#     "Accept-Language": "zh-CN,zh;q=0.9"
# }
# res = requests.get("https://zh.wikipedia.org/wiki/操作系统", headers = headers)

# print(res.text)


# import os
# from hanlp_restful import HanLPClient

# with open("res/cn/1.txt", 'r', encoding = "utf-8") as f:
#     text = f.read()

# HanLP = HanLPClient('https://www.hanlp.com/hanlp/v21/redirect', auth = '660ebfd6eaf668ab781bd519', language = 'zh')
# text = HanLP(text, tasks = 'tok/coarse').pretty_print()
# print(text)


# poter stemming
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer

# lemmatizer
lemmatizer = WordNetLemmatizer()

with open("res/en/2.txt", 'r', encoding = "utf-8") as f:
    text = f.read()
print("\033[91m[PREVIOUS]\033[0m")
print(text)
print("========================================")
# tokenize and pos tagging
words = word_tokenize(text)
pos_tags = pos_tag(words)

lemmas = []
for word, pos in pos_tags:
    lemma = lemmatizer.lemmatize(word, pos=pos[0].lower()) if pos[0].lower() in ['a', 'n', 'v'] else lemmatizer.lemmatize(word)
    lemmas.append(lemma)

# print lemmatized text
print("\033[92m[PROCESSED]\033[0m")
print(*lemmas, sep=' ')
