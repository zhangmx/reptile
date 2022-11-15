# -*- coding: utf-8 -*-
# 参考 https://github.com/rsain/GitHub-Crawler
import csv
import json
import logging
import math
import sys
import time
import os

import requests

# OUTPUT_FOLDER = "/your/folder/GitHub-Crawler/"  # Folder where ZIP files will be stored
OUTPUT_FOLDER = os.path.join(os.getcwd(), "out")
OUTPUT_CSV_FILE = os.path.join(OUTPUT_FOLDER, "projects.csv")  # Path to the CSV file generated as output
OUTPUT_CSV_FILE_LOST = os.path.join(OUTPUT_FOLDER, "projects_lost.csv")  # Path to the CSV file generated as output

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler(os.path.join(OUTPUT_FOLDER, "projects.log"))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

#############
# Constants #
#############

URL = "https://tzxm.zjzwfw.gov.cn/publicannouncement.do?method=queryItemList"  # The basic URL

QUERYDATA = {
    "pageFlag": "null",
    "pageNo": 0,
    "area_flag": 1,
    "deal_code": "",
    "item_name": "光伏"
}

DELAY_BETWEEN_QUERIES = 4  # The time to wait between different queries to GitHub (to avoid be banned)

TITLE = ['项目代码', '项目状态', '办理时间', '项目名称', '审批监管事项', '办理状态', '管理部门', 'projectuuid',
         'SENDID']

HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '70',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'JSESSIONID=E162FD2E7981254220D17C362B5D752A; '
              'SERVERID=e59cb5cf86bbeeff4488d95f21828741|1668405732|1668405582',
    'Host': 'tzxm.zjzwfw.gov.cn',
    'Origin': 'https://tzxm.zjzwfw.gov.cn',
    'Referer': 'https://tzxm.zjzwfw.gov.cn/tzxmweb/zwtpages/resultsPublicity/notice_of_publicity.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/107.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}


#############
# Functions #
#############

def get_data_from_url(url, data):
    """ Given a URL it returns its body """
    response = requests.post(url, data, headers=HEADERS)
    # return response.json()
    return response.text


def get_data_more_time(page, projects, count_of_repositories):
    logger.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " more time No. of pages = " + str(page))
    QUERYDATA['pageNo'] = page
    try:
        data = json.loads(get_data_from_url(URL, QUERYDATA))
        # data = json.loads(json.dumps(getUrl(URL, QUERYDATA)))
        data_length = len(data[0]['itemList'])

        if len(data[0]['itemList']) > 0:
            logger.info("there are :" + str(data_length) + " items in page " + str(page))
            for item in data[0]['itemList']:
                count_of_repositories = count_of_repositories + 1
                projects.writerow(item.values())
        else:
            logger.info("No data in page " + str(page))

    except Exception as e:
        logger.info("Error with page " + str(page))
        logging.exception(e)
    finally:
        return count_of_repositories


########
# MAIN #
########
def main(page=1):
    # To save the number of repositories processed
    count_of_repositories = 0

    # Output CSV file which will contain information about repositories
    csv_file = open(OUTPUT_CSV_FILE, 'w')
    projects = csv.writer(csv_file, delimiter=',')
    projects.writerow(TITLE)

    data = json.loads(get_data_from_url(URL, QUERYDATA))

    number_of_pages = int(math.ceil(float(data[0]['counts']) / 10.0))
    logger.info("Number of pages: " + str(number_of_pages))

    if page == 1:
        # save data to csv
        data_length = len(data[0]['itemList'])
        logger.info("there are :" + str(data_length) + "items in first page ")

        for item in data[0]['itemList']:
            count_of_repositories = count_of_repositories + 1
            projects.writerow(item.values())

    logger.info("Sleeping " + str(DELAY_BETWEEN_QUERIES) + " seconds before the new query ...")
    time.sleep(DELAY_BETWEEN_QUERIES)

    for i in range(page, number_of_pages + 1):
        logger.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "No. of pages = " + str(i))
        QUERYDATA['pageNo'] = i
        try:
            data = json.loads(get_data_from_url(URL, QUERYDATA))
            # data = json.loads(json.dumps(getUrl(URL, QUERYDATA)))
            data_length = len(data[0]['itemList'])

            if len(data[0]['itemList']) > 0:
                logger.info("there are :" + str(data_length) + " items in page " + str(i))
                for item in data[0]['itemList']:
                    count_of_repositories = count_of_repositories + 1
                    projects.writerow(item.values())
            else:
                logger.info("No data in page " + str(i))

                # TODO save the page number to a file

                # get data one more time
                count_of_repositories = get_data_more_time(i, projects, count_of_repositories)

        except Exception as e:
            logger.info("Error with page " + str(i))
            logging.exception(e)

            # TODO save the page number to a file

            # data = json.loads(getUrl(URL, QUERYDATA))
            # # data = json.loads(json.dumps(getUrl(URL, QUERYDATA)))
            # # save data to csv
            # for item in data[0]['itemList']:
            #     count_of_repositories = count_of_repositories + 1
            #     projects.writerow(item.values())

        logger.info("Sleeping " + str(DELAY_BETWEEN_QUERIES) + " seconds before the new query ...")
        time.sleep(DELAY_BETWEEN_QUERIES)

        # for debug only
        # if i == 3:
        #     break

    logger.info("DONE! " + str(count_of_repositories) + " projects have been processed.")
    csv_file.close()


def get_all_lost_page():
    pages = [288, 289, 290, 1037]
    fetch_all_lost_page(pages)


def fetch_all_lost_page(pages=None):
    count_of_repositories = 0

    csv_file = open(OUTPUT_CSV_FILE_LOST, 'w')
    projects = csv.writer(csv_file, delimiter=',')
    projects.writerow(TITLE)

    if pages is None:
        pages = []
    for page in pages:
        count_of_repositories = fetch_specific_page_data(page, projects, count_of_repositories)

    logger.info("DONE! " + str(count_of_repositories) + " projects have been processed.")
    csv_file.close()


def fetch_specific_page_data(page, projects, count_of_repositories):
    QUERYDATA['pageNo'] = page
    try:
        data = json.loads(get_data_from_url(URL, QUERYDATA))
        data_length = len(data[0]['itemList'])

        if len(data[0]['itemList']) > 0:
            logger.info("there are :" + str(data_length) + " items in page " + str(page))
            for item in data[0]['itemList']:
                count_of_repositories = count_of_repositories + 1
                projects.writerow(item.values())
        else:
            logger.info("No data in page " + str(page))

            # TODO save the page number to a file

            # get data one more time
            count_of_repositories = get_data_more_time(page, projects, count_of_repositories)

    except Exception as e:
        logger.info("Error with page " + str(page))
        logging.exception(e)

        # TODO save the page number to a file
    return count_of_repositories


# main
if __name__ == "__main__":
    main()
