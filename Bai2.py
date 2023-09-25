# -*- coding: utf-8 -*-
"""
Created on 9/25/2023 10:52 PM
@author: Thanh An
"""
import mysql.connector

def execute_queries(mydb, queries):
    mycursor = mydb.cursor()
    for query in queries:
        mycursor.execute(query)
        result = mycursor.fetchall()
        for row in result:
            print(row)

def main():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="12345678",
        database="mydatabase"
    )

    queries = [
        "SELECT title FROM crawl WHERE time = 'Thứ Hai, ngày 25/09/2023 21:00 PM (GMT+7)'",
        "SELECT title FROM crawl WHERE author = 'Đỗ Anh - Tuấn Hải ([Tên nguồn])'",
        "SELECT title FROM crawl WHERE type = 'Bóng Đá'"
    ]

    execute_queries(mydb, queries)

    mydb.close()

if __name__ == "__main__":
    main()
