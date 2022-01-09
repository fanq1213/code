import requests
from bs4 import BeautifulSoup
import time


child_domin = "https://pic.netbian.com"
for page_index in range(2,162):
    domain = f"https://pic.netbian.com/4kdongman/index_{page_index}.html"
    resp = requests.get(domain)
    resp.encoding = "gbk"  # 指定字符集
    page = resp.text
    # 解析page的内容
    context = BeautifulSoup(page, "html.parser")
    # 获取页面中的缩略图的路径
    aList = context.find("ul", class_="clearfix").find_all("a")
    # 获取跳转页面的路径
    for a in aList:
        child_url = child_domin + a.get("href")
        # 获取跳转后的页面源码
        child_resp = requests.get(child_url)
        child_resp.encoding = "gbk"  # 指定字符集
        child_page = child_resp.text
        # 解析二级页面获取到真正的图片的url
        child_context = BeautifulSoup(child_page, "html.parser")
        # 获取uri
        img_uri = child_context.find("div", class_="photo-pic").find("img").get("src")
        img_url = child_domin + img_uri
        img_resp = requests.get(img_url)
        img_name = img_url.split("/")[-1]
        # 下载图片 并将图片写入文件夹内
        with open("img/" + img_name, mode="wb") as f:
            f.write(img_resp.content)
        print("over!!!", img_name)
        time.sleep(0.5)
f.close()
print("all over!!!")
