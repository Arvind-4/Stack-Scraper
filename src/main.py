from requests_html import HTML
import pandas as pd
import time
import pathlib
import requests

def clean_data(text, keyname=None):
    if keyname == "Votes":
        return text.replace("\nvotes", "")
    if keyname == "Tags":
        return text.replace("\n", ",")
    else:
        return text

def parse_tagged_page(html):
    question_summaries = html.find(".question-summary")

    key_names = ["Question", "Votes", "Tags"]
    class_needed = [".question-hyperlink", ".vote", ".tags"]

    data = []

    for question_element in question_summaries:
        question_data = {}
        for i, _class in enumerate(class_needed):
            sub_element = question_element.find(_class, first=True)
            keyname = key_names[i]
            question_data[keyname] = clean_data(sub_element.text, keyname=keyname)
        data.append(question_data)
    return data


def extract_data_from_url(url):
    r = requests.get(url)
    if r.status_code not in range(200, 299):
        return []

    html_str = r.text
    html = HTML(html=html_str)

    datas = parse_tagged_page(html)
    return datas

def scrape_tag(tag="python", query_filter="Votes", max_pages=50, page_size=25):
    datas = []
    base_url = "https://stackoverflow.com/questions/tagged/"
    for p in range(max_pages):
        page_num = p + 1
        url = f"{base_url}{tag}?tab={query_filter}&page={page_num}&pagesize={page_size}"
        datas += extract_data_from_url(url)

    return datas

input_tag = input('Enter a language(eg. python, javascripts...): ')

data = scrape_tag(tag=input_tag)

df = pd.DataFrame(data)

BASE_DIR = pathlib.Path(__file__).resolve().parent
FOLDER_PATH = BASE_DIR / 'Data'
FOLDER_PATH.mkdir(parents=True, exist_ok=True)

FILE_NAME = f'{input_tag.capitalize()}.csv'
SAVE_PATH = f'{FOLDER_PATH}\\{FILE_NAME}'

df.to_csv(SAVE_PATH, index=False)