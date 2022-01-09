import csv
import requests
import re

# 准备url
domian = "https://www.dytt89.com"

# 准备heater
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}
resp = requests.get(domian, headers=headers)
# 指定字符集
resp.encoding = "gb2312"
# 获取首页中2021必看热片的跳转连接
obj = re.compile(r"2021必看热片.*?<ul>.*?<li><a href='(?P<uris>.*?)</ul>", re.S)
result = obj.finditer(resp.text)
# 获取a标签中的href连接
href = re.compile(r"<li><a href='(?P<uri>.*?)'", re.S)
# 循环构造完整连接
data = re.compile(r'◎片　　名(?P<movie>.*?)<br />.*?<td '
                  r'style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<download>.*?)">', re.S)
f = open("电影天堂必看热片.csv", mode="a", encoding="utf-8", newline='')
csvwriter = csv.writer(f)
# 写入表头
csvwriter.writerow(["电影名称", "下载连接"])
for it in result:
    uris = href.finditer(it.group("uris"))
    for uri in uris:
        url = domian + uri.group("uri")
        # 在从urls中循环获取二级页面内的下载路径
        child_resp = requests.get(url, headers=headers)
        child_resp.encoding = "gb2312"
        result_data = data.search(child_resp.text)
        dic = result_data.groupdict()
        csvwriter.writerow(dic.values())
f.close()
print("下载完成。。。")