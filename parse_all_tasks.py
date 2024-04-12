from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import time
import re
import json
from typing import Dict, List, Set, Union, Callable


difficult_levels = {'8 kyu': 'Beginner', '7 kyu': 'Beginner', '6 kyu': 'Easy', '5 kyu': 'Easy', 'Easy': 'Easy',
                    '4 kyu': 'Medium', '3 kyu': 'Medium', 'Medium': 'Medium', '2 kyu': 'Hard', '1 kyu': 'Hard',
                    'Hard': 'Hard'}

with open('all_tags.txt', 'r') as file_tags:
    tags = json.loads(file_tags.read())

with open('tasks_blank.txt', 'r') as file:
    all_tasks = json.loads(file.read())


def get_one_task_leetcode(link: Tag, tasks: Dict[str, Set[str]], difficulty_level: str) -> None:
    if link:
        new_task = link.find('a').get('href')
        task_url = urls['lc']['url'] + new_task[1:]
        if difficulty_level in tasks:
            tasks[difficulty_level].add(task_url)
        else:
            tasks[difficulty_level] = {task_url}


def get_tasks_from_leetcode(url_for_parse: str, tasks: Dict[str, Set[str]]) -> None:
    s = Service(executable_path="C:/usr/local/bin/chromedriver.exe")
    browser = webdriver.Chrome(service=s)
    browser.get(url_for_parse)
    time.sleep(0.3)
    if browser.title == 'Page Not Found - LeetCode':
        return
    try:
        browser.find_element(By.CLASS_NAME, 'title-cell__ZGos')
        soup = BeautifulSoup(browser.page_source, 'lxml')
        task_blocks = soup.find_all('tr')
        for task in task_blocks:
            if task.find('i', class_="fa-lock") is None:
                difficulty = task.find('span', class_='label')
                if difficulty:
                    difficulty_level = difficulty.text
                    link = task.find('div', class_="title-cell__ZGos")
                    get_one_task_leetcode(link, tasks, difficulty_level)
        browser.quit()
    except NoSuchElementException:
        browser.quit()
        get_tasks_from_leetcode(url_for_parse, tasks)


def get_one_task_codewars(div: Tag, tasks: Dict[str, Set[str]], difficulty_level: str) -> None:
    link = div.find('a', href=re.compile(r'python$'))
    href = link['href']
    task_url = urls['cw']['url'] + href[1:]
    if difficulty_level in tasks:
        tasks[difficulty_level].add(task_url)
    else:
        tasks[difficulty_level] = {task_url}


def get_tasks_from_codewars(url_for_parse: str, tasks: Dict[str, Set[str]]) -> None:
    response = requests.get(url_for_parse)
    soup = BeautifulSoup(response.content, 'html.parser')
    task_divs = soup.find_all('div', class_='list-item-kata')
    for div in task_divs:
        link = div.find('div', class_='inner-small-hex')
        if link and link.find('span'):
            get_one_task_codewars(div, tasks, difficult_levels[link.find('span').string])


def slugify_tag(tag: str, site_url: Dict[str, Union[str, Callable]]) -> str:
    tag = tag.replace('(', '').replace(')', '').split()
    if site_url['name'] == 'leetcode':
        return '-'.join(tag)
    elif site_url['name'] == 'codewars':
        return '?q=&tags=' + '%20'.join(tag)


urls = {'lc': {'name': 'leetcode',
               'url': 'https://leetcode.com/',
               'postfix': 'tag/',
               'parse_function': get_tasks_from_leetcode
               },
        'cw': {'name': 'codewars',
               'url': 'https://www.codewars.com/',
               'postfix': 'kata/search/python',
               'parse_function': get_tasks_from_codewars
               }}


def get_tasks_by_category(site_url: Dict[str, Union[str, Callable]], subcategories: List[str]) -> Dict[str, Set[str]]:
    all_tasks_for_category = {}
    for category in subcategories:
        parse_url = site_url['url'] + site_url['postfix'] + slugify_tag(category, site_url)
        site_url['parse_function'](parse_url, all_tasks_for_category)
        time.sleep(0.5)
    return all_tasks_for_category


def add_to_db(category: str, subcategory: str, found_tasks: Dict[str, List[str]]) -> None:
    global all_tasks
    for difficulty, tasks in found_tasks.items():
        if difficulty in all_tasks[category][subcategory]:
            all_tasks[category][subcategory][difficulty] = list(all_tasks[category][subcategory][difficulty]) + tasks
        else:
            all_tasks[category][subcategory][difficulty] = tasks


def tasks_to_json(dict_tasks: Dict[str, Union[Set[str], List[str]]]) -> Dict[str, List[str]]:
    for difficulty, tasks in dict_tasks.items():
        dict_tasks[difficulty] = list(tasks)
    return dict_tasks


def parse_it(current_url: Dict[str, Union[str, Callable]], all_tags: Dict[str, Dict[str, List[str]]]) -> None:
    for category_key, category_val in all_tags.items():
        for subcategory_key, subcategory_val in category_val.items():
            current_tasks = get_tasks_by_category(current_url, subcategory_val)
            current_tasks = tasks_to_json(current_tasks)
            add_to_db(category_key, subcategory_key, current_tasks)


def get_db_imitation(tasks: Dict[str, Dict[str, Dict[str, List[str]]]]) -> None:
    tasks = json.dumps(tasks, indent=4)
    with open('tasks_db.txt', 'w') as tasks_file:
        tasks_file.write(tasks)


if __name__ == '__main__':
    start_time = time.time()
    for url in urls.values():
        print(f"{url['name']} parsing...")
        parse_it(url, tags)
        print(f"Time {url['name']}: {time.time() - start_time}")
        start_time = time.time()

    get_db_imitation(all_tasks)
