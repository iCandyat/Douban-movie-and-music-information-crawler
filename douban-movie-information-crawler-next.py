import requests
from pyquery import PyQuery as pq
import re


def doulist_crawler(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        doc = pq(response.text)
        doulist = []

        field_map = {
            '导演': 'director',
            '主演': 'starring',
            '类型': 'genre',
            '制片国家/地区': 'region',
            '年份': 'year'
        }

        for item in doc(".doulist-item").items():
            title_elem = item(".title a")
            item_dict = {
                'title': title_elem.text(),
                'detail_url': title_elem.attr("href"),
                'rating': item(".rating_nums").text(),
                'rating_count': extract_rating_count(item)  # 修正此处
            }

            # 优化后的字段解析逻辑
            abstract = {}
            for line in item('div.abstract').text().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    if key in field_map:
                        abstract[field_map[key]] = value.strip()

            item_dict.update(abstract)
            doulist.append(item_dict)

        return doulist

    except requests.RequestException as e:
        print(f"请求异常: {str(e)}")
        return []
    except Exception as e:
        print(f"解析异常: {str(e)}")
        return []


def extract_rating_count(item):  # 改为独立函数
    """提取评分人数"""
    try:
        count_text = item('.rating span:contains("人评价")').text()
        return int(re.search(r'\d+', count_text).group())
    except (AttributeError, ValueError):
        return 0


if __name__ == "__main__":
    movie_list = doulist_crawler('https://www.douban.com/doulist/240962/')
    print(movie_list[:2])  # 输出前两条记录验证