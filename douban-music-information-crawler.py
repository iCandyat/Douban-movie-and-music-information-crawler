import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

# 设置请求头
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

# 初始化数据列表
music_name = []
music_url = []
music_star = []
music_star_people = []
music_singer = []
music_pub_date = []
music_type = []
music_media = []
music_style = []

# 爬取每一页的数据
for i in range(10):
    url = 'https://music.douban.com/top250'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    musics = soup.select('.item')

    for music in musics:
        name = music.select('.pl2 a')[0].text.replace('\n', '').replace(' ', '').strip()
        music_name.append(name)
        url = music.select('.pl2 a')[0]['href']
        music_url.append(url)
        star = music.select('.rating_nums')[0].text
        music_star.append(star)
        star_people = music.select('.pl')[1].text.strip().replace(' ', '').replace('人评价', '').replace('(', '').replace(')', '')
        music_star_people.append(star_people)
        infos = music.select('.pl')[0].text.strip().split('/')
        music_singer.append(infos[0])
        music_pub_date.append(infos[1])
        music_type.append(infos[2])
        music_media.append(infos[3])
        music_style.append(infos[4])
df = pd.DataFrame({
    '专辑名称': music_name,
    '专辑链接': music_url,
    '专辑评分': music_star,
    '评分人数': music_star_people,
    '歌手': music_singer,
    '发行日期': music_pub_date,
    '类型': music_type,
    '介质': music_media,
    '曲风': music_style
})
df.to_csv('douban_music_top250.csv', encoding='utf_8_sig')
