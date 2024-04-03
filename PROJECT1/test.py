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


# sender = '744317484@qq.com'  # 发送邮箱
# receivers = ['tst17@my.swjtu.edu.cn']  # 接收邮箱
# # auth_code = uslovcpsshmjbfbc"  # 授权码

# message = MIMEText('Python发送邮件', 'plain', 'utf-8')
# message['From'] = Header("Sender<%s>" % sender)  # 发送者
# message['To'] = Header("Receiver<%s>" % receivers[0])  # 接收者

# subject = 'Python SMTP 邮件测试'
# message['Subject'] = Header(subject, 'utf-8')


# try:
#     server = smtplib.SMTP_SSL('smtp.qq.com', 465)
#     server.login(sender, auth_code)
#     server.sendmail(sender, receivers, message.as_string())
#     print("邮件发送成功")
#     server.close()
# except smtplib.SMTPException:
#     print("Error: 无法发送邮件")

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9"
}
res = requests.get("https://zh.wikipedia.org/wiki/操作系统", headers = headers)

print(res.text)