# -*- coding: utf-8 -*-

import csv
import os
import re
import json
import logging
import sys

OUTPUT_FOLDER = os.path.join(os.getcwd(), "out")
OUTPUT_CSV_FILE = os.path.join(OUTPUT_FOLDER, "projects_2w.csv")  # Path to the CSV file generated as output
OUTPUT_CSV_FILE_CLEAN = os.path.join(OUTPUT_FOLDER, "projects_2w_clean.csv")  # Path to the CSV file generated as output

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler(os.path.join(OUTPUT_FOLDER, "projects_clean.log"))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

TITLE = ['项目代码', '项目状态', '办理时间', '项目名称', '审批监管事项', '办理状态', '管理部门', 'projectuuid',
         'SENDID', '项目名称(改)', '省', '市', '区', '单位', '规模']

# https://github.com/modood/Administrative-divisions-of-China
AREA_CODE_JSON = os.path.join(os.getcwd(), "pca-code.json")  # Path to the JSON file containing the area code

with open(AREA_CODE_JSON, 'r', encoding='utf-8') as b:
    area_code_json_data = json.load(b)


def find_area_code(area_code):
    location = []
    for item in area_code_json_data:
        if item['code'] == area_code[0:2]:
            location.append(item['name'])
            for city in item['children']:
                if city['code'] == area_code[0:4]:
                    location.append(city['name'])
                    for area in city['children']:
                        if area['code'] == area_code:
                            location.append(area['name'])
                            break
    return location


def test_find_area_code():
    logger.info(find_area_code('331023'))
    logger.info(find_area_code('330782'))
    logger.info(find_area_code('330481'))


def main():
    csv_file = open(OUTPUT_CSV_FILE_CLEAN, 'w')
    projects = csv.writer(csv_file, delimiter=',')

    with open(OUTPUT_CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        for index, row in enumerate(reader):
            if index == 0:
                projects.writerow(TITLE)
                continue
            logger.info(index)
            logger.info(row[0])
            logger.info(row[3])
            logger.info(row[0][5:11])

            # replace '千瓦' to 'KW'
            no_chinese = row[3].replace('千瓦', 'KW').replace('兆瓦', 'MW')
            row.append(no_chinese)

            #  find 'XX市 区'
            area_code = row[0][5:11]
            logger.info(area_code)
            local = find_area_code(area_code)
            logger.info(local)
            if len(local) == 3:
                row.append(local[0])
                row.append(local[1])
                row.append(local[2])
            elif len(local) == 2:
                row.append(local[0])
                row.append(local[1])
                row.append('')
            elif len(local) == 1:
                row.append(local[0])
                row.append('')
                row.append('')
            else:
                row.append('')
                row.append('')
                row.append('')

            # reg split with   \d*\.?\d+[a-zA-Z]+
            regex = r'(\d*\.?\d+[a-zA-Z]+)'
            res = re.split(regex, no_chinese)
            logger.info(res)

            if len(res) == 1:
                row.append(res[0])
                row.append('')
            else:
                row.append(res[0])
                row.append(res[1])

            projects.writerow(row)

            # if index == 10:
            #     break


# main
if __name__ == "__main__":
    main()
