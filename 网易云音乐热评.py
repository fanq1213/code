import json

import requests
from Crypto.Cipher import AES
from base64 import b64encode
import csv
import time

"""
js中赋值的方法
 e9f.data = j9a.cq9h({
                params: bVj0x.encText,
                encSecKey: bVj0x.encSecKey
            })
js中加密请求数据的方法  
    获取一个随机的字符串          
    function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    使用AES就行对称加密
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b) b=0CoJUm6Qyw8W8jud
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a) a=传入的数据 
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    使用RSA非对称加密
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    真正的加密方法
    function d(d, e, f, g) { ) 
        var h = {}
          , i = a(16); 是一个16位的字符串 "8nPYfHhrGEIu5JjP"
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }
"""
url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="

data = {
    "rid": "R_SO_4_569213220", # 歌曲对应的id
    "threadId": "R_SO_4_569213220",
    "pageNo": "1",
    "pageSize": "20",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "csrf_token": ""
}
# 用来加密data用的参数
f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
g = "0CoJUm6Qyw8W8jud"
i = "8nPYfHhrGEIu5JjP"
e = "010001"


# 由于i可以debug获取到，所以d方法中的c方法最终的结果就是一个字符串

def get_encSecKey():
    return "73e99ee217cdb4d07b6947635c74047bff778823dd433ab870e0f11c2e7056add7bf7a4daf7c598f96192e5559c17ceee8d267fe7e9121511d224e8b74138b49e94e9983768e75641adccbda73b5b9d9b5809a82277dc017ed4f557561bdaab8b80cfed70a84538c2dbf02a637c462b842c0f7fa2443589a85395d99aaff22c3"


# 加密过程
def enc_params(data, key):
    iv = "0102030405060708"
    data = to_16(data)
    aes = AES.new(key=key.encode("utf-8"), IV=iv.encode('utf-8'), mode=AES.MODE_CBC)  # 创建加密器
    bs = aes.encrypt(data.encode("utf-8"))  # 加密, 加密的内容的长度必须是16的倍数
    return str(b64encode(bs), "utf-8")  # 转化成字符串返回,


param = "QKjNbInsQdG7ignRVvh+DrvYYtPrFNeMMMdriP7RWLRSG3Pgbj1/Rk39K+BpukpSwbFY9JIkmWGBAxCW2WLlkDtI0aP0S9JodTb4YX8wLOsTB/+I6XVIHtAKd204b4wGYFtspC6oYK147otyETw9qe+HsMpYA3ZkawcTxqrx1+ns4Kh5mgra2IFlaKDw9jGRG4m5tPKGItxNOjBf0awMfkUYHJqCqzd/Ed2KsH6X8sbgthlDzMvn8Qz+6REbmpxy1GOVuPWmZKVPAFFjNFuqpHEPfZxUduV8xp35go+d44A="


# 转化成16的倍数, 位下方的加密算法服务
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


# 把参数进行加密
def get_params(data):  # 默认这里接收到的是字符串
    first = enc_params(data, g)
    second = enc_params(first, i)
    return second  # 返回的就是params

# 时间戳转成时间
def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime
def get_data():
    resp = requests.post(url, data={
        "params": get_params(json.dumps(data)),
        "encSecKey": get_encSecKey()
    })
    return resp.json()['data']['hotComments']



if __name__ == '__main__':
    # 准备文件
    f = open("网易云音乐热评.csv", mode="a", encoding="utf-8", newline='')
    csvwriter = csv.writer(f)
    # 写入表头
    csvwriter.writerow(["昵称", "热评", "点赞数", "评论时间"])
    # 获取数据
    hotComments = get_data()

    for hotComment in hotComments:
        csvwriter.writerow([hotComment["user"]["nickname"],hotComment["content"],hotComment["likedCount"],timeStamp(hotComment["time"])])
    f.close()
    print("over!!!")

