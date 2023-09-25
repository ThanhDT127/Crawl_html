"""
Created on 9/21/2023 1:07 AM
@author: Thanh An
"""
from bs4 import BeautifulSoup
import urllib
import requests
import time
import json
import re
import pyodbc
import mysql.connector


def check_none(element):
    if element is not None:
        return element.get_text().strip()
    return None


def save_data(data):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="12345678",
        database="mydatabase"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO Crawl (title,content,time,author,img_url,type) VALUES (%s,%s,%s,%s,%s,%s)"
    values = (
        data["Tên bài báo: "],
        data["Nội dung: "],
        data["Thời gian đăng bài: "],
        data["Tác giả:"],
        data["URl-image:"],
        data["Type:"]
    )
    # mycursor.execute("ALTER TABLE Crawl MODIFY COLUMN time VARCHAR(255);")
    mycursor.execute(sql, values)
    mydb.commit()
    mycursor.close()
    mydb.close()

def Parser_html(url,category):
    # truy cập vào url
    try:
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
    except:
        print("lỗi kết nối đến url", req)

    # lấy nội dung
    title = soup.title.string
    content = soup.find("div", id="left")
    time = content.find("time")
    time = check_none(time)

    if content is not None:
        strong_element = content.find("strong")
        content_details = check_none(strong_element)

    author_div = soup.find("div", class_="nguontin nguontinD bld mrT10 mrB10 fr flex-1 text-right margin-left-10")
    if author_div is None:
        author_div = soup.find("div", class_="nguontin nguontinD")
    author = check_none(author_div)
    if author is not None:
        author = author.replace("Theo", "").strip()

    img_tags = soup.find("article", {"class": "cate-24h-foot-arti-deta-info"})
    img_url = None
    if img_tags is None:
        img_tags = soup.find("section", {"class": "cate-24h-foot-main"})
    if img_tags is not None and img_tags.find("img", src=True) is not None:
        img_url = img_tags.find("img", src=True)["src"]
        print(img_url)

    Json = {
        "Tên bài báo: ": title,
        "Nội dung: ": content_details,
        "Thời gian đăng bài: ": time,
        "Tác giả:": author,
        "URl-image:": img_url,
        "Type:":category
    }
    return Json


def Cralw_html():
    category_urls = {
        "Bóng đá": "https://www.24h.com.vn/bong-da-c48.html",
        "Thế giới": "https://www.24h.com.vn/tin-tuc-quoc-te-c415.html",
        "Pháp luật": "https://www.24h.com.vn/an-ninh-hinh-su-c51.html",
        "Kinh doanh": "https://www.24h.com.vn/kinh-doanh-c161.html",
        "Đàn ông": "https://www.24h.com.vn/dan-ong-c1038.html",
        "Làm đẹp": "https://www.24h.com.vn/lam-dep-c145.html",
        "Đời sống Showbiz": "https://www.24h.com.vn/doi-song-showbiz-c729.html",
        "Thời trang Hi-tech": "https://www.24h.com.vn/thoi-trang-hi-tech-c407.html",
        "Ẩm thực": "https://www.24h.com.vn/am-thuc-c460.html",
        "Xe máy - xe đạp": "https://www.24h.com.vn/xe-may-xe-dap-c748.html",
        "Công nghệ thông tin": "https://www.24h.com.vn/cong-nghe-thong-tin-c55.html",
        "Du lịch": "https://www.24h.com.vn/du-lich-24h-c76.html"
    }

    category_urls_2 = {
        "Thời trang Hi-tech": "https://www.24h.com.vn/thoi-trang-hi-tech-c407.html",
        "Ẩm thực": "https://www.24h.com.vn/am-thuc-c460.html",
        "Xe máy - xe đạp": "https://www.24h.com.vn/xe-may-xe-dap-c748.html",
        "Công nghệ thông tin": "https://www.24h.com.vn/cong-nghe-thong-tin-c55.html",
        "Du lịch": "https://www.24h.com.vn/du-lich-24h-c76.html"
    }

    for category, url in category_urls.items():
        print(category)
        try:
            req = requests.get(url)
            soup = BeautifulSoup(req.text, "html.parser")
        except:
            print("lỗi kết nối đến url", req)
        url_web = soup.find_all("section", {"class": "cate-24h-foot-box-news-hightl box-news-hightl-ftb"})
        if category in category_urls_2:
            url_web = soup.find_all("div", {
                "class": "cate-24h-foot-box-live-news-hightl cate-24h-car-news-hightl margin-top-10"})
        seen_links = set()
        # truy cập vào từng link
        for link in url_web:
            div_sec = link.find("div", {"class": "row"})
            div_element = link.find_all("a", href=True, limit=10)
            count = 0
            for links in div_element:
                href_value = links['href']
                if href_value not in seen_links:
                    count += 1
                    seen_links.add(href_value)
                    data_json = Parser_html(href_value,category)
                    save_data(data_json)
                    # lưu vào file json
                    try:
                        file = category + str(count) + ".json"
                        with open(file, "w+", encoding="utf-8") as Json_file:
                            json.dump(data_json, Json_file, ensure_ascii=False, indent=4)
                            print("Đã lưu thông tin vào file ", file)
                    except json.JSONDecodeError as e:
                        print("Lỗi lưu vào file json.")


def main():
    # time_duration_minutes = 10
    # time_duration_seconds = time_duration_minutes * 60
    # while True:
        Cralw_html()
        # time.sleep(time_duration_seconds)


if __name__ == "__main__":
    main()
