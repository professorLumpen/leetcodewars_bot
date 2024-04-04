from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup
import time
import re
import json


tags = {'Data Structures': {'Data Structures': {'Data Structures'},
                            'Stacks and Queues': {'Queues', 'Stacks', 'Stack', 'Queue', 'Monotonic Stack',
                                                  'Monotonic Queue'},
                            'Heaps': {'Heaps', 'Priority Queues', 'Heap (Priority Queue)'},
                            'Sets': {'Sets', 'Ordered Set'},
                            'Hash Tables': {'Hash Table', 'Hash Function'},
                            'Arrays': {'Arrays', 'Lists', 'Array', 'Prefix Sum', 'Suffix Array'},
                            'Strings': {'Strings', 'String', 'String Matching', 'Trie', 'Rolling Hash'},
                            'Linked Lists': {'Linked Lists', 'Linked List', 'Doubly-Linked List'},
                            'Trees': {'Trees', 'Binary Search Trees', 'Binary Trees', 'Tree', 'Binary Tree',
                                      'Segment Tree',
                                      'Binary Search Tree', 'Binary Indexed Tree', 'Minimum Spanning Tree'},
                            'Graphs': {'Graph Theory', 'Graphs', 'Depth-First Search', 'Breadth-First Search', 'Graph',
                                       'Shortest Path',
                                       'Topological Sort', 'Strongly Connected Component', 'Biconnected Component',
                                       'Eulerian Circuit'}
                            },
        'Basic Algorithms': {'Dynamic Programming': {'Dynamic Programming'},
                             'Greedy': {'Greedy'},
                             'Two Pointers': {'Two Pointers'},
                             'Sliding Window': {'Sliding Window'},
                             'Divide and Conquer': {'Divide and Conquer'},
                             'Recursion': {'Recursion', 'Backtracking'},
                             'Memoization': {'Memoization'},
                             'Sorting': {'Sorting', 'Merge Sort', 'Bucket Sort', 'Counting Sort', 'Radix Sort'},
                             'Searching': {'Searching', 'Filtering', 'Binary Search', 'Quickselect', 'Counting',
                                           'Enumeration'},
                             'Bits': {'Binary', 'Bits', 'Bit Manipulation', 'Bitmask'},
                             'Logic Algorithms': {'Logic', 'Performance', 'Restricted'},
                             'Other Algorithms': {'Date Time', 'Networks', 'Scheduling', 'Union Find',
                                                  'Rejection Sampling', 'Line Sweep', 'Reservoir Sampling'},
                             'Common Algorithms': {'Algorithms', 'Fundamentals'}
                             },
        'Math': {'Math': {'Mathematics', 'Math', 'Physics', 'Number Theory'},
                 'Algebra': {'Algebra', 'Linear Algebra', 'Matrix'},
                 'Combinatorics': {'Combinatorics', 'Permutations'},
                 'Geometry': {'Geometry'},
                 'Discrete Math': {'Set Theory'},
                 'Probability and Statistics': {'Probability', 'Statistics', 'Game Theory',
                                                'Probability and Statistics'}},

        'Programming': {'Functional Programming': {'Functional Programming'},
                        'Object-oriented Programming': {'Object-oriented Programming', 'Metaprogramming'},
                        'Design Patterns': {'Decorator', 'Iterators', 'Singleton', 'Design Patterns', 'Design',
                                            'Iterator'},
                        'Regular Expressions': {'Regular Expressions'},
                        'Threads': {'Asynchronous', 'Threads', 'Concurrency', 'Data Stream'},
                        'Debugging': {'Debugging', 'Refactoring'},
                        'Meta-Programming': {'Angular', 'Esoteric Languages', 'Compilers', 'Interpreters',
                                             'Domain Specific Languages', 'Language Features', 'State Machines',
                                             'Tutorials', 'Randomized'},
                        },
        'Language Usage': {'Big Data': {'Artificial Intelligence', 'Data Science', 'Machine Learning', 'NumPy',
                                        'Data Frames'},
                           'Security': {'Cryptography', 'Ciphers', 'Security', 'Parsing', 'Web Scraping', 'Unicode'},
                           'Puzzles and Graphics': {'ASCII Art', 'Puzzles', 'Graphics', 'Image Processing'},
                           'Simulation': {'Cellular Automata', 'Genetic Algorithms', 'Simulation'},
                           'Interactive': {'Riddles', 'Game Solvers', 'Games', 'Interactive', 'Brainteaser'},
                           },

        'Other Technologies': {'Backend': {'Backend', 'Flask'},
                               'JSON': {'JSON'},
                               'Databases': {'SQL', 'Databases', 'MongoDB', 'Database'},
                               'Shell': {'Shell'}
                               }}

difficult_levels = {'8 kyu': 'Beginner', '7 kyu': 'Beginner', '6 kyu': 'Easy', '5 kyu': 'Easy', 'Easy': 'Easy',
                    '4 kyu': 'Medium', '3 kyu': 'Medium', 'Medium': 'Medium', '2 kyu': 'Hard', '1 kyu': 'Hard',
                    'Hard': 'Hard'}

all_tasks = {'Data Structures': {'Data Structures': {},
                                 'Stacks and Queues': {},
                                 'Heaps': {},
                                 'Sets': {},
                                 'Hash Tables': {},
                                 'Arrays': {},
                                 'Strings': {},
                                 'Linked Lists': {},
                                 'Trees': {},
                                 'Graphs': {}
                                 },
             'Basic Algorithms': {'Dynamic Programming': {},
                                  'Greedy': {},
                                  'Two Pointers': {},
                                  'Sliding Window': {},
                                  'Divide and Conquer': {},
                                  'Recursion': {},
                                  'Memoization': {},
                                  'Sorting': {},
                                  'Searching': {},
                                  'Bits': {},
                                  'Logic Algorithms': {},
                                  'Other Algorithms': {},
                                  'Common Algorithms': {}
                                  },
             'Math': {'Math': {},
                      'Algebra': {},
                      'Combinatorics': {},
                      'Geometry': {},
                      'Discrete Math': {},
                      'Probability and Statistics': {}},

             'Programming': {'Functional Programming': {},
                             'Object-oriented Programming': {},
                             'Design Patterns': {},
                             'Regular Expressions': {},
                             'Threads': {},
                             'Debugging': {},
                             'Meta-Programming': {},
                             },
             'Language Usage': {'Big Data': {},
                                'Security': {},
                                'Puzzles and Graphics': {},
                                'Simulation': {},
                                'Interactive': {},
                                },

             'Other Technologies': {'Backend': {},
                                    'JSON': {},
                                    'Databases': {},
                                    'Shell': {}
                                    }}


def get_one_task_leetcode(link, tasks, difficulty_level):
    if link:
        new_task = link.find('a').get('href')
        task_url = urls['lc']['url'] + new_task[1:]
        if difficulty_level in tasks:
            tasks[difficulty_level].add(task_url)
        else:
            tasks[difficulty_level] = {task_url}


def get_tasks_from_leetcode(url_for_parse, tasks):
    browser = webdriver.Chrome()
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


def get_one_task_codewars(div, tasks, difficulty_level):
    link = div.find('a', href=re.compile(r'python$'))
    href = link['href']
    task_url = urls['cw']['url'] + href[1:]
    if difficulty_level in tasks:
        tasks[difficulty_level].add(task_url)
    else:
        tasks[difficulty_level] = {task_url}


def get_tasks_from_codewars(url_for_parse, tasks):
    response = requests.get(url_for_parse)
    soup = BeautifulSoup(response.content, 'html.parser')
    task_divs = soup.find_all('div', class_='list-item-kata')
    for div in task_divs:
        link = div.find('div', class_='inner-small-hex')
        if link and link.find('span'):
            get_one_task_codewars(div, tasks, difficult_levels[link.find('span').string])


def slugify_tag(tag, site_url):
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


def get_tasks_by_categories(site_url, subcategories):
    all_tasks_for_category = {}
    for category in subcategories:
        parse_url = site_url['url'] + site_url['postfix'] + slugify_tag(category, site_url)
        site_url['parse_function'](parse_url, all_tasks_for_category)
        time.sleep(0.5)
    return all_tasks_for_category


def add_to_db(category, subcategory, found_tasks):
    global all_tasks
    for difficulty, tasks in found_tasks.items():
        if difficulty in all_tasks[category][subcategory]:
            all_tasks[category][subcategory][difficulty] = list(all_tasks[category][subcategory][difficulty]) + tasks
        else:
            all_tasks[category][subcategory][difficulty] = tasks


def tasks_to_json(dict_tasks):
    for difficulty, tasks in dict_tasks.items():
        dict_tasks[difficulty] = list(tasks)
    return dict_tasks


def parse_it(current_url, all_tags):
    for category_key, category_val in all_tags.items():
        for subcategory_key, subcategory_val in category_val.items():
            current_tasks = get_tasks_by_categories(current_url, subcategory_val)
            current_tasks = tasks_to_json(current_tasks)
            add_to_db(category_key, subcategory_key, current_tasks)


def get_db_imitation(tasks):
    tasks = json.dumps(tasks, indent=4)
    with open('tasks_db.txt', 'w') as file:
        file.write(tasks)


if __name__ == '__main__':
    start_time = time.time()
    for url in urls.values():
        print(f"{url['name']} parsing...")
        parse_it(url, tags)
        print(f"Time {url['name']}: {time.time() - start_time}")
        start_time = time.time()

    get_db_imitation(all_tasks)
