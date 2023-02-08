import csv
import requests
import re

url = 'https://steamcommunity.com/market/listings/730/Clutch%20Case'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

response = requests.get(url, headers=headers)

result = re.search('<script.*?line1=(.*?);.*?</script>', response.text, re.S)

path = r'D:\大四上\数据科学\csgo.txt'

with open(path, 'w', encoding='utf-8') as f:
    f.write(result.group(1))

file = open(path)
file_read = file.read()

table = str.maketrans('', '', '":+[]')
file_translate = file_read.translate(table)

lst = file_translate.split(',')

list_time = []
list_price = []
list_num = []

i = 0
j = 0
while i < len(lst):
    list_time.insert(j, lst[i])
    list_price.insert(j, lst[i + 1])
    list_num.insert(j, lst[i + 2])
    i = i + 3
    j = j + 1

with open('ak47list.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['time', 'price', 'number'])
    for i in range(len(list_time)):
        writer.writerow([list_time[i], list_price[i], list_num[i]])
