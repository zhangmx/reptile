# reptile crawler

~~爬虫~~

## 网页爬虫，有很多技术方案

https://github.com/bda-research/node-crawler

https://scrapy.org/
https://github.com/scrapy/scrapy

## 上面这些都没用到

由于有数据请求URL，直接通过URL请求JSON数据，然后解析数据并保存。

## reg tool

https://regex101.com/

## setup

```shell
pip install -r requirements.txt
```

## run

采集：
```shell
cd python-request
python getDataFromGov.py
```

采集完成后，out目录下的log日志文件中找到报错的页码。如果没有报错，直接执行下面的清理数据脚本。

补充数据的时候，把页码填写到:

```python

def get_all_lost_page():
    pages = [288, 289, 290, 1037] # 遗漏的页码
    fetch_all_lost_page(pages)

```

然后修改main函数执行这个函数。

清理数据：

```shell
cd python-request
python clean_data.py
```
