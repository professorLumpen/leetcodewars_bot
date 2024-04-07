import requests
from bs4 import BeautifulSoup
import json


urls = {'lc': {'name': 'leetcode',
               'url': 'https://leetcode.com/',
               'postfix': 'problemset/',
               'payload': True},
        'cw': {'name': 'codewars',
               'url': 'https://www.codewars.com/',
               'postfix': 'kata/search/python',
               'payload': False}}


with open('headers.txt', 'r') as headers_file:
    headers = json.loads(headers_file.read())

with open('payload.txt', 'r') as data_file:
    payload = data_file.read()


def get_tags_from_response(response, params):
    soup = BeautifulSoup(response.content, 'lxml')
    tags = []
    if params['name'] == 'leetcode':
        tag_divs = soup.find_all('div', class_='group m-[10px] flex items-center')
        for div in tag_divs:
            link = div.find('span', class_='whitespace-nowrap')
            tags.append(link.string)
    elif params['name'] == 'codewars':
        tag_divs = soup.find('sl-select', id='tags_filter').find_all('sl-menu-item')
        for div in tag_divs:
            link = div['value']
            tags.append(link)
    return tags


def write_tags_on_file(tags, params):
    with open(f'{params["name"]}_tags.txt', 'w') as file:
        for elem in tags:
            file.write(elem + '\n')


def get_tags_by_urls(urls_param, heads, pay_data):
    for params in urls_param.values():
        pay_data = pay_data if params['payload'] else ''
        response = requests.get(params['url'] + params['postfix'], headers=heads, data=pay_data)
        if response.status_code == 200:
            tags = get_tags_from_response(response, params)
            write_tags_on_file(tags, params)
        else:
            print('Error ', response.status_code)


if __name__ == '__main__':
    get_tags_by_urls(urls, headers, payload)
