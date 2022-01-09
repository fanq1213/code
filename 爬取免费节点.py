import time
import aiofiles as aiofiles
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}

def getRoles(url):
    # 准备好参数配置
    opt = Options()
    opt.add_argument("--headless")
    opt.add_argument("--disbale-gpu")

    web = Chrome(options=opt)  # 把参数配置设置到浏览器中

    web.get(url)

    time.sleep(2)
    # el = web.find_element_by_xpath('/html/body/div[2]/div/div/main/div/div/div/div[2]/article[1]/div[1]/h2/a')
    el = web.find_element_by_xpath('//*[@id="Blog1"]/div[2]/article[1]/div[1]/h2/a')
    href_url = el.get_attribute('href')

    print(href_url)

    web.get(href_url)

    time.sleep(2)

    roles =  web.find_elements_by_tag_name('span')

    for role in roles:
        if(role.get_attribute('role') == "presentation"):
            with open("免费节点.txt", mode="a", encoding="utf-8") as f:
                f.write(role.text + "\n")


if __name__ == '__main__':
    url = "https://www.cfmem.com/search/label/free"
    roles = getRoles(url)

    print("over!!!")