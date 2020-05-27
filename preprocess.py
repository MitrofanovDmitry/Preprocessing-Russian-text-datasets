import os
import re
import argparse
import ijson
import requests
import json
import time
from tqdm import tqdm
from bs4 import BeautifulSoup

texts = []
files = []
re_for_russian_letters = re.compile(
    r'[^.,:?!1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя\'\-\(\) ]',
    re.U
)
chars_to_replace = {
    ' ': " ", 
    '%': " процентов", 
    '\u2009': " ", 
    '\u200a': " ", 
    '\u200d': "", 
    '\u200f': "", 
    '\u2028': "",
    '«': "'", 
    '»': "'",
    '"': "'",
    "&quot;":"'",
    ' -- ': '', 
    'î': 'i', 
    'ø': 'o',
    'š': 's', 
    'á': 'a', 
    'ä': 'a', 
    'ç': 'c', 
    'è': 'e', 
    'é': 'e', 
    'ë': 'е', 
    'ё': 'e',
    'ï': 'i', 
    'ô': 'o', 
    'ö': 'o', 
    'ü': 'u', 
    'ɢ': 'g', 
    'і': 'i', 
    'ї': 'i', 
    'ӧ': 'o',
    '•': '',
    '    ': ' ', 
    '   ': ' ', 
    '  ': ' ',    
    '‑': '-', 
    '–': '-', 
    '—': '-', 
    '―': '-',
    '─': '-'   
}
def pr(dataset):
    with open(dataset+'.csv', 'w', encoding="utf-8") as output:
        with open('source_data/'+dataset+'/metatable.csv', encoding='utf-8') as f:
            next(f)
            for line in f:
                parts = line.strip().split('	')
                if not(parts[1] in files):
                    files.append(parts[1])

                    txt_path = os.path.join('source_data/'+dataset+'/texts/', '{}.txt'.format(parts[1].lower())) 
                    #if (os.path.exists(txt_path)):

                    with open(txt_path, encoding='utf-8') as f2:
                        line3 = ""
                        if (dataset == "lenta"):
                            line2 = f2.readlines(2)
                            if (len(line2)>1):
                                line3 = line2[1]
                        else:
                            for line2 in f2:
                                line3 = line3 + line2.replace("\n"," ")
                        if (line3):
                            for key, value in chars_to_replace.items():
                                parts[2] = parts[2].replace(key, value)
                            tex = re.sub(re_for_russian_letters, '', parts[2])
                            output.write(tex + '|')
                            for key, value in chars_to_replace.items():
                                line3 = line3.replace(key, value)
                            line3 = re.sub(re_for_russian_letters, '', line3)
                            if (dataset == "kp"):
                                line4 = line3.split('jwplayer')
                                line3 = line4[0]
                            output.write(line3 + "\n")

def meduza():
    with open('meduza.csv', 'w', encoding="utf-8") as output:
        stream = 'https://meduza.io/api/v3/search?chrono=news&locale=ru&page={page}&per_page=24'
        news = 'https://meduza.io/api/v3/{url}'
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.3411.123 YaBrowser/16.2.0.2314 Safari/537.36'
        headers = {'User-Agent' : user_agent }
        for page in tqdm(range(878,3000)):
            # Достаём страницы
            ans = requests.get(stream.format(page = page), headers=headers).json()
            documents = ans['documents']
            for url,data in documents.items():
                try:
                    time.sleep(0.5)
                    text = requests.get(news.format(url = url), headers=headers).json()
                    text1 = text['root']['content']['body']

                    text1 = re.sub('<[A-Za-z\/][^>]*>', '', text1)
                    text1 = re.sub(r'\s+', ' ', text1)
                    #soup = BeautifulSoup(text1)
                    #text1 = soup.get_text()
                    for key, value in chars_to_replace.items():
                        text1 = text1.replace(key, value)
                    text1 = re.sub(re_for_russian_letters, '', text1)
                    text1 = re.sub('View this post.*?\)\(\)', '', text1)
                    text1 = re.sub('\(function.*?\(\)\)', '', text1)
                    text1 = re.sub("Rectangle 30.*?origin: 'https:meduza.io'", '', text1)
                    text1 = re.sub(".Spoiler background.*?\) \)", '', text1)
                    text1 = re.sub("pic.twitter.*?20[0-1][0-9]", '', text1)
                    text1 = re.sub(".RichBlock.*?line-height: 27px", '', text1)
                    text1 = re.sub(r'\s+', ' ', text1)
                    name = data["title"]
                    for key, value in chars_to_replace.items():
                        name = name.replace(key, value)
                    name = re.sub(re_for_russian_letters, '', name)
                    output.write(name + '|'+text1 + "\n")
                except Exception:
                    continue   


def lenta2():                                 
    with open('lenta2.csv', 'w', encoding="utf-8") as output:
        titles = []
        objects = ijson.items(open('./source_data/lenta.json', encoding='utf-8'), 'item')

        items = (o for o in objects)

        for item in items:
            name = item['page'][0]['metaTitle']
            for key, value in chars_to_replace.items():
                name = name.replace(key, value)
            name = re.sub(re_for_russian_letters, '', name)
            output.write(name + '|')            
            text = item['page'][0]['plaintext']
            for key, value in chars_to_replace.items():
                text = text.replace(key, value)
            text = re.sub(re_for_russian_letters, '', text)
            output.write(text + "\n")
def habr(): 
    with open('habr.csv', 'w', encoding="utf-8") as output:
        for page in tqdm(range(1440,463293)):
            time.sleep(0.1)
            r = requests.get('https://habr.com/ru/post/' +str(page) + '/')
            soup = BeautifulSoup(r.text, 'html5lib')
            text = ""
            if not soup.find("span", {"class": "post__title-text"}):
                text = ""
            else:
                name = soup.find("span", {"class": "post__title-text"}).text
                for key, value in chars_to_replace.items():
                    name = name.replace(key, value)
                name = re.sub(re_for_russian_letters, '', name)
                output.write(name + '|')
                text = soup.find("div", {"class": "post__text"}).text
                text = re.sub(r'\s+', ' ', text)
                for key, value in chars_to_replace.items():
                    text = text.replace(key, value)
                text = re.sub(re_for_russian_letters, '', text)
                output.write(text + "\n")

def fontanka():                                
    with open('fontanka.csv', 'w', encoding="utf-8") as output:
        for y in range(2007,2017):
            with open('source_data/Fontanka/metatable_'+str(y)+'.csv', encoding='utf-8') as f:
                next(f)
                for line in f:
                    parts = line.strip().split('	')
                    if not(parts[1] in files):
                        files.append(parts[1])

                        txt_path = os.path.join('source_data/Fontanka/texts/',str(y), '{}.txt'.format(parts[1].lower())) 
                        #if (os.path.exists(txt_path)):

                        with open(txt_path, encoding='utf-8') as f2:
                            line3 = ""
                            for line2 in f2:
                                line3 = line3 + line2.replace("\n"," ")
                            if (line3):
                                for key, value in chars_to_replace.items():
                                    parts[2] = parts[2].replace(key, value)
                                tex = re.sub(re_for_russian_letters, '', parts[2])
                                output.write(tex + '|')
                                for key, value in chars_to_replace.items():
                                    line3 = line3.replace(key, value)
                                line3 = re.sub(re_for_russian_letters, '', line3)
                                output.write(line3 + "\n")    
def proza():                                
    with open('proza.csv', 'w', encoding="utf-8") as output:
        for y in range(2005,2011):
            with open('source_data/proza_ru/metatable_'+str(y)+'.txt', encoding='utf-8') as f:
                next(f)
                for line in f:
                    parts = line.strip().split('	')
                    if not(parts[7] in files):
                        files.append(parts[7])

                        txt_path = os.path.join('source_data/proza_ru/',parts[7]) 
                        #if (os.path.exists(txt_path)):

                        with open(txt_path, encoding='utf-8') as f2:
                            line3 = ""
                            for line2 in f2:
                                line3 = line3 + line2.replace("\n"," ")
                            if (line3):
                                for key, value in chars_to_replace.items():
                                    parts[2] = parts[2].replace(key, value)
                                tex = re.sub(re_for_russian_letters, '', parts[2])
                                output.write(tex + '|')
                                for key, value in chars_to_replace.items():
                                    line3 = line3.replace(key, value)
                                line3 = re.sub(re_for_russian_letters, '', line3)
                                output.write(line3 + "\n")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datasets", type=str, 
                        default="arzamas",
                        help="name dataset")
    args = parser.parse_args()
    if (args.datasets=="fontanka"): # https://tatianashavrina.github.io/taiga_site/downloads
        fontanka()
    if (args.datasets=="proza"): # https://tatianashavrina.github.io/taiga_site/downloads
        proza()        
    elif (args.datasets=="lenta2"): # https://github.com/yutkin/Lenta.Ru-News-Dataset
        lenta2()
    elif (args.datasets=="meduza"): 
        meduza()
    elif (args.datasets=="habr"):
        habr()       
    else:
        pr(args.datasets)           # https://tatianashavrina.github.io/taiga_site/downloads
                