import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["SabayNewsData"]  # Create/use a database
collection = db["NewsCollection"]  # Create/use a collection


def save_news(url, title, i, j):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    target_div = soup.find("div", class_="content-detail")
    p_tags = target_div.find_all("p")
    texts = []
    for p in p_tags:
        texts.append(p.get_text())
    collection.insert_one({"url": url, "title": title.strip(), "paragraphs": texts})


def work_on_page(i):
    soup = BeautifulSoup(
        requests.get(
            "https://news.sabay.com.kh/ajax/topics/technology/" + str(i)
        ).content,
        "html.parser",
    )
    divs = soup.find_all("div", class_="list-item")
    for j in range(len(divs)):
        div = divs[j]
        title = div.find("span", class_="web").get_text()
        url = div.find("a").get("href").split("#")[0]
        save_news(url, title, i, j)


for i in range(50):
    print(i + 1)
    work_on_page(i + 1)
