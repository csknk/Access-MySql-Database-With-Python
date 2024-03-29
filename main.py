#!/usr/bin/env python3
import sys
import pymysql
import logger
from config import mysql
import csv

conn = None

def open_connection():
    global conn
    try:
        if (conn is None or not conn.open):
            conn = pymysql.connect(mysql['host'], mysql['user'], mysql['password'], mysql['db'])
    except:
#        logger.error("ERROR: Could not connect to database.")
        sys.exit()

def get_records(cpt):
    try:
        open_connection()
        with conn.cursor() as cur:
            sql = "SELECT post_date, post_title, post_content FROM wp_posts WHERE post_type = '{}'".format(cpt)
            cur.execute(sql)
            results = cur.fetchall()
            cur.close()
            conn.close()
    except Exception as e:
        print(e)
    finally:
        print ("Query successful.")
        header = ['date', 'title', 'content']
        with open('{}.csv'.format(cpt), 'wt') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(header)
            for result in results:
                csv_writer.writerow(result)


def main():
    cpts = ['training', 'resource', 'report', 'chapter', 'event', 'course', 'staff-resource', 'post', 'page']
    for cpt in cpts:
        get_records(cpt)

if __name__ == '__main__':
    main()
