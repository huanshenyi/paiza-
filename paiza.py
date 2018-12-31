import requests
from lxml import etree
from pyecharts import Bar
import numpy as np


#ループする時に使う
BASE_DOMAIN = "https://paiza.jp/career/job_offers/dev_language/"
HEADERS = {
    "user-agent": ""
}
ALL_DATA = []

def get_detail_urls(url):
    #全てurlを入れる配列
    urls=[]
    urls.append(url)
    response = requests.get(url, headers=HEADERS)
    text = response.text
    #ページングの中のurlも全部入る配列
    html = etree.HTML(text)
    max_page = html.xpath("//div[@class='nav clearfix']//li/a/text()")[3]
    for x in range(2, int(max_page)+1):
        urls.append(url+"?page="+str(x))
    return urls

def crawler(keyword):
    base_url = "https://paiza.jp/career/job_offers/dev_language/{}"

    url = base_url.format(keyword)
    response = get_detail_urls(url)

    return response

def data_search(url):
    datas=[]
    response = requests.get(url, headers=HEADERS)
    text = response.content.decode("utf-8")
    html = etree.HTML(text)
    #ここ一回親domだけを取得してもいい気がする
    # 这个里面出问题
    company = html.xpath("//div[@class='c-job_offer-box  c-job_offer-box--career']//div[@class='c-job_offer-box__body']//div[@class='c-job_offer-recruiter']//h4[@class='c-job_offer-recruiter__name']//a/text()")
    money = html.xpath("//div[@class='c-job_offer-box  c-job_offer-box--career']//div[@class='c-job_offer-box__body']//div[@class='c-job_offer-condition']//table[@class='c-job_offer-detail']//td[@class='c-job_offer-detail__description']//strong/text()")
    moneys=map(lambda x: x[0:3], money)
    for c, m in zip(company, moneys):
        datas.append({"company": c, "money": int(m)})

    return datas

def sabu(keyword):
    companys = []
    #base_html全てのページが入る

    base_html = crawler(keyword)
    for url in base_html:
        data = data_search(url)
        companys.append(data)
    return companys

def main():
    keyword = input("最高基本年収知りたい言語を入力してください:")
    companys = sabu(keyword)
    b=[]
    for x in companys:
        b.extend(x)

    def money_lank(companys):
        for key,x in enumerate(companys):
            if(type(x)) != int:
                print(key,x)
            return x['money']

    b.sort(key=lambda data: data['money'])
    #b.sort(key=money_lank, reverse=True)


    datas = b[0:15]

    cities = list(map(lambda x: x['company'], datas))
    temps = list(map(lambda x: x['money'], datas))

    npmany = round(np.mean(temps))

    chart = Bar("paiza求人年収ランキング", keyword,width=1200)
    chart.add("%s平均年収%s"%(keyword,npmany), cities, temps,xaxis_interval=0, xaxis_rotate=20,yaxis_formatter="万円")
    chart.render("paiza%s.html"%keyword)

if __name__== "__main__":
    main()

