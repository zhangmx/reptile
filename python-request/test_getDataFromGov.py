# -*- coding: utf-8 -*-
# 参考 https://github.com/rsain/GitHub-Crawler
from getDataFromGov import *


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
    test_data_structure()
