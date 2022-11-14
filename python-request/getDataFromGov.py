# -*- coding: utf-8 -*-
# 参考 https://github.com/rsain/GitHub-Crawler
import json
from os import getcwd

import wget
import time
import csv
import requests
import math
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('projects.log')
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
# OUTPUT_FOLDER = "/your/folder/GitHub-Crawler/"  # Folder where ZIP files will be stored
OUTPUT_FOLDER = getcwd() + "/out/"
OUTPUT_CSV_FILE = OUTPUT_FOLDER + "projects.csv"  # Path to the CSV file generated as output

TITLE = ['项目代码', '项目状态', '办理时间', '项目名称', '审批监管事项', '办理状态', '管理部门', 'projectuuid',
         'SENDID']

HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '70',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'JSESSIONID=E162FD2E7981254220D17C362B5D752A; SERVERID=e59cb5cf86bbeeff4488d95f21828741|1668405732|1668405582',
    'Host': 'tzxm.zjzwfw.gov.cn',
    'Origin': 'https://tzxm.zjzwfw.gov.cn',
    'Referer': 'https://tzxm.zjzwfw.gov.cn/tzxmweb/zwtpages/resultsPublicity/notice_of_publicity.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}


#############
# Functions #
#############

def getUrl(url, data):
    """ Given a URL it returns its body """
    response = requests.post(url, data, headers=HEADERS)
    # return response.json()
    return response.text


########
# MAIN #
########
def main(page=1):
    # To save the number of repositories processed
    countOfRepositories = 0

    # Output CSV file which will contain information about repositories
    csv_file = open(OUTPUT_CSV_FILE, 'w')
    projects = csv.writer(csv_file, delimiter=',')
    projects.writerow(TITLE)

    data = json.loads(getUrl(URL, QUERYDATA))

    # data = json.loads(json.dumps(getUrl(URL, QUERYDATA)))

    numberOfPages = int(math.ceil(float(data[0]['counts']) / 10.0))
    print("Number of pages: " + str(numberOfPages))

    if page == 1:
        # save data to csv
        for item in data[0]['itemList']:
            countOfRepositories = countOfRepositories + 1
            projects.writerow(item.values())

    print("Sleeping " + str(DELAY_BETWEEN_QUERIES) + " seconds before the new query ...")
    time.sleep(DELAY_BETWEEN_QUERIES)

    for i in range(page, numberOfPages + 1):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "No. of pages = " + str(i))
        QUERYDATA['pageNo'] = i
        try:
            data = json.loads(getUrl(URL, QUERYDATA))
            # data = json.loads(json.dumps(getUrl(URL, QUERYDATA)))
            for item in data[0]['itemList']:
                countOfRepositories = countOfRepositories + 1
                projects.writerow(item.values())
        except:
            print("Error with page " + str(i))

            # data = json.loads(getUrl(URL, QUERYDATA))
            # # data = json.loads(json.dumps(getUrl(URL, QUERYDATA)))
            # # save data to csv
            # for item in data[0]['itemList']:
            #     countOfRepositories = countOfRepositories + 1
            #     projects.writerow(item.values())

        print("Sleeping " + str(DELAY_BETWEEN_QUERIES) + " seconds before the new query ...")
        time.sleep(DELAY_BETWEEN_QUERIES)

        # for debug only
        # if i == 3:
        #     break

    print("DONE! " + str(countOfRepositories) + " projects have been processed.")
    csv_file.close()


def test_data_structure(page=1):
    # get file content from /target-site/res.txt
    with open('../target-site/res.txt', 'r') as f:
        data = json.loads(f.read())
        # data = json.loads(json.dumps(f.read()))
    #

    # print current time
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print()
    print(page)
    print()

    print(data)

    print(data[0]['counts'])
    print()
    print(data[0]['itemList'])
    print()
    print(data[0]['itemList'][0])
    print()
    logger.info(data[0]['itemList'][0]['deal_code'])  # 项目代码
    logger.info(data[0]['itemList'][0]['DEAL_STATE'])  # 项目状态
    logger.info(data[0]['itemList'][0]['DEAL_TIME'])  # 办理时间
    logger.info(data[0]['itemList'][0]['apply_project_name'])  # 项目名称
    logger.info(data[0]['itemList'][0]['ITEM_NAME'])  # 审批监管事项
    logger.info(data[0]['itemList'][0]['DEAL_NAME'])  # 办理状态
    logger.info(data[0]['itemList'][0]['DEPT_NAME'])  # 管理部门
    logger.info(data[0]['itemList'][0]['projectuuid'])
    logger.info(data[0]['itemList'][0]['SENDID'])

    time.sleep(DELAY_BETWEEN_QUERIES)

    logger.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    csv_file = open(OUTPUT_CSV_FILE, 'w')
    repositories = csv.writer(csv_file, delimiter=',')
    repositories.writerow(TITLE)
    # repositories.writerow(data[0]['itemList'][0].values())
    # repositories.writerow(data[0]['itemList'][1].values())

    for item in data[0]['itemList']:
        repositories.writerow(item.values())

    csv_file.close()


# main
if __name__ == "__main__":
    # main()
    test_data_structure()
