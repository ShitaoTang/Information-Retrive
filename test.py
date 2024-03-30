import requests
import re

start_url = "https://www.ietf.org/rfc/"
res = requests.get(start_url).text

rule_en = re.compile(r"<tr><td.*?href=\"(?P<name>.*?)\.txt\".*?</td></tr>")
urls = rule_en.finditer(res)

for item in urls:
    r = item.groupdict()
    print(r['name'])