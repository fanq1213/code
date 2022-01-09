import requests
import csv
import re

# 准备heater
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}
lits = ["name", "year", "country", "category", "score", "number", "quote"]
# 准备文件
f = open("豆瓣电影 Top 250.csv", mode="a", encoding="utf-8", newline='')
csvwriter = csv.writer(f)
# 写入表头
csvwriter.writerow(["电影名称", "年份", "国家", "分类", "评分", "评分人数"])
for uri in range(0, 250, 25):
    url = f"https://movie.douban.com/top250?start={uri}"
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    # 准备正则匹配
    obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)'
                     r'</span>.*?<p class="">.*?<br>(?P<year>.*?)&nbsp;/&nbsp;(?P<country>.*?)&nbsp;/&nbsp;(?P<category>.*?)</p>'
                     r'.*?<div class="star">.*?<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
                     r'<span>(?P<number>.*?)人评价</span>', re.S)
    result = obj.finditer(resp.text)
    # 循环格式化数据，并且写入文件中
    for it in result:
        dic = it.groupdict()
        dic['year'] = dic['year'].strip()
        dic['category'] = dic['category'].strip()
        csvwriter.writerow(dic.values())
f.close()
print("写入完成。。。")
