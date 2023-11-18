import json
import re
from bs4 import BeautifulSoup
import numpy as np
from collections import Counter


def handler(file_name):
    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row
        site = BeautifulSoup(text, 'html.parser')

        item = dict()
        item['category'] = site.find_all("span", string=re.compile("Категория:"))[0].getText().split(':')[1].strip()
        item['title'] = site.find_all("h1")[0].getText().strip()
        item['author'] = site.find_all("p")[0].getText().strip()
        item['pages'] = int(site.find_all("span", string=re.compile("Объем:"))[0].getText().split()[1].strip())
        item['year'] = int(site.find_all("span", string=re.compile("Издано"))[0].getText().split()[2].strip())
        item['ISBN'] = site.find_all("span", string=re.compile("ISBN:"))[0].getText().split(':')[1].strip()
        item['description'] = site.find_all("p", string=re.compile("Описание"))[0].getText().replace('Описание',
                                                                                                     '').strip()
        item['img_url'] = site.find_all("img")[0]["src"]
        item['rating'] = float(site.find_all("span", string=re.compile("Рейтинг:"))[0].getText().split(':')[1].strip())
        item['views'] = int(site.find_all("span", string=re.compile("Просмотры:"))[0].getText().split(':')[1].strip())

        return item


items = []
for i in range(1, 999):
    file_name = f"./input/1/{i}.html"
    items.append(handler(file_name))

with open("./output/1_result_all.json", 'w', encoding='utf-8') as json_file:
    json_file.write(json.dumps(sorted(items, key=lambda x: x['views'], reverse=True), ensure_ascii=False, indent=2))

filtered_items = [item for item in items if item['pages'] > 450]
with open('./output/1_filtered_result.json', 'w', encoding='utf-8') as json_file:
    json.dump(filtered_items, json_file, ensure_ascii=False, indent=2)

view_stat = {}
view_values = [item['views'] for item in items]
view_stat['sum'] = int(np.sum(view_values))
view_stat['min'] = int(np.min(view_values))
view_stat['max'] = int(np.max(view_values))
view_stat['avg'] = float(np.mean(view_values))

category_values = [item['category'] for item in items]
category_stat = Counter(category_values)

result_data = {
    'views_stat': view_stat,
    'category_stat': category_stat
}

with open('./output/1_stats.json', 'w', encoding='utf-8') as json_file:
    json.dump(result_data, json_file, ensure_ascii=False, indent=2)
