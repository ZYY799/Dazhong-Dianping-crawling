import os
import csv
import re

import requests

from bs4 import BeautifulSoup

file_exists = os.path.isfile('评论.csv')

headers = {
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
  "Cache-Control": "max-age=0",
  "Connection": "keep-alive",
  "Referer": "https://verify.meituan.com/",
  "Sec-Fetch-Dest": "document",
  "Sec-Fetch-Mode": "navigate",
  "Sec-Fetch-Site": "cross-site",
  "Sec-Fetch-User": "?1",
  "Upgrade-Insecure-Requests": "1",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
  "sec-ch-ua-mobile": "?0"
}

cookies={
  "_lxsdk_cuid": "18e69f73b3dc8-0227d3fb55f1c6-4c657b58-13c680-18e69f73b3dc8",
  "_lxsdk": "18e69f73b3dc8-0227d3fb55f1c6-4c657b58-13c680-18e69f73b3dc8",
  "_hc.v": "315e914a-da94-23ba-5ee7-d53b7be2e520.1711176105",
  "WEBDFPID": "9yx82v5yx0v851uzz64wy62022194z2281v3z9y492x97958vw654zxv-2026536109663-1711176109663YISQUWGfd79fef3d01d5e9aadc18ccd4d0c95072601",
  "ua": "%E7%82%B9%E5%B0%8F%E8%AF%848793679062",
  "ctu": "b764f0d09af3d6815ec1347f5abe8697c5387a09b46bab9327703cec4d39bdc8",
  "s_ViewType": "10",
  "_lx_utm": "utm_source%3Dbing%26utm_medium%3Dorganic",
  "fspop": "test",
  "Hm_lvt_602b80cf8079ae6591966cc70a3940e7": "1711371129,1711549464,1711610409,1712021318",
  "cy": "9",
  "cye": "chongqing",
  "qruuid": "d82cdc41-a5bc-43ce-b5b7-55627945c4d1",
  "dplet": "da8bb30ae8f350587cb5d2ab7d25ad98",
  "dper": "0202a52862b5a97dce9909f8ed02c8587f812fa09d9d61dcf5d16dfe6cab36353234cc527900a8e1dedc2ec2e0443d2d3099e90563ff6da20bdf00000000fa1e000027e3a82beb0099a936d485f7ad9ff494d338e17087c19e53877bfd135290c0f073461884e3d69dcbeebb5aeedb9f4af1",
  "ll": "7fd06e815b796be3df069dec7836c3df",
  "Hm_lpvt_602b80cf8079ae6591966cc70a3940e7": "1712021653",
  "_lxsdk_s": "18e9c6c2626-b3f-db2-db1%7C%7C98"
}


with open('评论.csv', mode='a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(['简短评论', '完整评论'])

    for i in range(1, 2):
        url = f"https://www.dianping.com/shop/G5AC3G5C4EYZ0ixU/review_all/p{i}"
        response = requests.get(url=url, headers=headers, cookies=cookies)

        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')

            # 提取简短评论
            try:
                comment_short = soup.find('div', class_='review-truncated-words').text.strip()
                comment_short = re.sub(r'(展开评价|收起评价)', '', comment_short) 
                comment_short = re.sub(r'\s+', ' ', comment_short)
            except AttributeError:
                comment_short = '无'

            # 提取完整评论
            try:
                comment_all = soup.find('div', class_='review-words Hide').text.strip()
                comment_all = re.sub(r'(展开评价|收起评价)', '', comment_all) 
                comment_all = re.sub(r'\s+', ' ', comment_all) 
            except AttributeError:
                comment_all = '无'

            print("简短评论：", comment_short)
            print("完整评论：", comment_all)

            # 将评论写入CSV文件
            writer.writerow([comment_short, comment_all])
        else:
            print(f"获取第{i}页数据失败。状态码: {response.status_code}")

