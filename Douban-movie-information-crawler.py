import requests
from pyquery import PyQuery as pq
import re

def doulist_crawler(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        doc = pq(response.text)
        doulist_item_doc = doc(".doulist-item")
        doulist = []

        for item in doulist_item_doc.items():
            item_dict = {}
            director = None
            starring = None
            genre = None
            region = None
            year = None

            detail_url = item(".title a").attr("href")
            title = item(".title a").text()
            rating_nums = item(".rating_nums").text()
            rating_count_text = item('.rating span:contains("人评价")').text()
            rating_count = int(re.search(r'\d+', rating_count_text).group(0))

            lines = item('div.abstract').text().split('\n')
            for line in lines:
                if '导演' in line:
                    director = line.split('导演:')[-1].strip()
                elif '主演' in line:
                    starring = line.split('主演:')[-1].strip()
                elif '类型' in line:
                    genre = line.split('类型:')[-1].strip()
                elif '制片国家/地区' in line:
                    region = line.split('制片国家/地区:')[-1].strip()
                elif '年份' in line:
                    year = line.split('年份:')[-1].strip()

            item_dict['director'] = director
            item_dict['starring'] = starring
            item_dict['genre'] = genre
            item_dict['region'] = region
            item_dict['year'] = year
            item_dict['detail_url'] = detail_url
            item_dict['title'] = title
            item_dict['rating_count'] = rating_count

            doulist.append(item_dict)

        return doulist
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return []

if __name__ == "__main__":
    movie_list = doulist_crawler('https://www.douban.com/doulist/240962/')
    print(movie_list)
