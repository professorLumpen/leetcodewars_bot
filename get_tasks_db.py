from typing import Union, Callable
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import re
import random
from get_tags import payload, headers


tags = {'Data Structures': {'Data Structures', 'Heaps', 'Priority Queues', 'Sets', 'Queues', 'Stacks', 'Hash Table',
                            'Heap (Priority Queue)', 'Stack', 'Queue', 'Ordered Set', 'Monotonic Stack',
                            'Hash Function', 'Monotonic Queue'},
        'Arrays and Strings': {'Arrays', 'Lists', 'Strings', 'Array', 'String', 'String Matching', 'Prefix Sum', 'Trie',
                               'Suffix Array', 'Rolling Hash'},
        'Linked Lists': {'Linked Lists', 'Linked List', 'Doubly-Linked List'},
        'Trees': {'Trees', 'Binary Search Trees', 'Binary Trees', 'Tree', 'Binary Tree', 'Segment Tree',
                  'Binary Search Tree', 'Binary Indexed Tree', 'Minimum Spanning Tree'},
        'Graphs': {'Graph Theory', 'Graphs', 'Depth-First Search', 'Breadth-First Search', 'Graph', 'Shortest Path',
                   'Topological Sort', 'Strongly Connected Component', 'Biconnected Component', 'Eulerian Circuit'},
        'Search and Sort': {'Searching', 'Sorting', 'Filtering', 'Sorting', 'Binary Search', 'Merge Sort',
                            'Quickselect', 'Bucket Sort', 'Counting Sort', 'Radix Sort'},
        'Dynamic Recursion': {'Dynamic Programming', 'Recursion', 'Memoization', 'Dynamic Programming', 'Backtracking',
                              'Recursion', 'Memoization'},
        'Base Algo': {'Fundamentals', 'Date Time', 'Binary', 'Bits', 'Networks', 'Functional Programming', 'Scheduling',
                      'Bit Manipulation', 'Bitmask', 'Counting', 'Enumeration'},
        'Common Algo': {'Algorithms', 'Greedy', 'Two Pointers', 'Sliding Window', 'Divide and Conquer'},
        'Logic': {'Logic', 'Performance', 'Restricted', 'Union Find', 'Rejection Sampling', 'Line Sweep',
                  'Reservoir Sampling'},
        'Games': {'ASCII Art', 'Puzzles', 'Riddles', 'Game Solvers', 'Games', 'Interactive', 'Brainteaser'},
        'Math': {'Algebra', 'Linear Algebra', 'Mathematics', 'Combinatorics', 'Number Theory', 'Geometry', 'Matrix',
                 'Physics', 'Statistics', 'Permutations', 'Probability', 'Set Theory', 'Math', 'Matrix',
                 'Number Theory', 'Geometry', 'Game Theory', 'Combinatorics', 'Probability and Statistics'},
        'Big Data': {'Artificial Intelligence', 'Data Science', 'Machine Learning', 'NumPy', 'Data Frames'},
        'OOP': {'Object-oriented Programming', 'Decorator', 'Iterators', 'Singleton', 'Design Patterns',
                'Metaprogramming', 'Design', 'Iterator'}, 'Regular Expressions': {'Regular Expressions'},
        'Encode and Simulation': {'Cellular Automata', 'Genetic Algorithms', 'Graphics', 'Image Processing',
                                  'Simulation', 'Parsing', 'Web Scraping', 'Cryptography', 'Ciphers', 'Security',
                                  'Unicode', 'Simulation'},
        'Meta': {'Angular', 'Esoteric Languages', 'Compilers', 'Interpreters', 'Domain Specific Languages',
                 'Language Features', 'State Machines', 'Tutorials', 'Debugging', 'Refactoring', 'Flask', 'JSON', 'SQL',
                 'Databases', 'MongoDB', 'Backend', 'Asynchronous', 'Concurrency', 'Threads', 'Database', 'Shell',
                 'Randomized', 'Concurrency', 'Data Stream'}}

difficulty = {'Basic': {'8 kyu', '7 kyu'},
              'Easy': {'6 kyu', '5 kyu', 'Easy'},
              'Medium': {'4 kyu', '3 kyu', 'Medium'},
              'Hard': {'2 kyu', '1 kyu', 'Hard'}}


def filter_by_difficulty_leetcode(cell, available_difficulty):
    new_cell = cell.find('span', class_='label')
    if new_cell and new_cell.text in available_difficulty:
        return True
    return False


def url_filter_leetcode(url_for_parse):
    response = requests.get(url_for_parse, headers=headers, data=payload)
    return response.status_code != 404


def url_filter_codewars(url_for_parse):
    response = requests.get(url_for_parse)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup.find('div', class_='list-item-kata')


def get_tasks_from_leetcode(url_for_parse, available_difficulty, tasks):
    browser = webdriver.Chrome()
    browser.get(url_for_parse)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    task_blocks = soup.find_all('tr')
    for task in task_blocks:
        if task.find('i', class_="fa-lock") is None and filter_by_difficulty_leetcode(task, available_difficulty):
            link = task.find('div', class_="title-cell__ZGos")
            if link:
                new_task = link.find('a').get('href')
                tasks.append(urls['lc']['url'] + new_task[1:])
    browser.quit()


def get_one_task_codewars(div, tasks):
    link = div.find('a', href=re.compile(r'python$'))
    href = link['href']
    tasks.append(urls['cw']['url'] + href)


def get_tasks_from_codewars(url_for_parse, available_difficulty, tasks):
    response = requests.get(url_for_parse)
    soup = BeautifulSoup(response.content, 'html.parser')
    task_divs = soup.find_all('div', class_='list-item-kata')
    for div in task_divs:
        link = div.find('div', class_='inner-small-hex').find('span')
        if link and link.string in available_difficulty:
            get_one_task_codewars(div, tasks)


def slugify_tag(tag: str, url: dict[str, Union[str, Callable]]) -> str:
    tag = tag.split()
    if url['name'] == 'leetcode':
        return '-'.join(tag)
    elif url['name'] == 'codewars':
        return '?q=&tags=' + '%20'.join(tag)


def get_user_choice(variants: list[str], title: str = 'Select an option:') -> str:
    print(title)
    for i, variant in enumerate(variants):
        print(f'{i} - {variant}')
    ans = input()

    while not ans.isdigit() or not (int(ans) in range(len(variants))):
        print(f'Enter digit in range 0-{len(variants) - 1}:')
        ans = input()

    if variants[int(ans)] == 'Random Choice':
        return random.choice(variants[:-1])

    return variants[int(ans)]


def get_random_tasks(count, tasks):
    random.shuffle(tasks)
    return tasks[:count]


urls = {'lc': {'name': 'leetcode',
               'url': 'https://leetcode.com/',
               'postfix': 'tag/',
               'parse_function': get_tasks_from_leetcode,
               'url_filter': url_filter_leetcode},
        'cw': {'name': 'codewars',
               'url': 'https://www.codewars.com/',
               'postfix': 'kata/search/python',
               'parse_function': get_tasks_from_codewars,
               'url_filter': url_filter_codewars}}


if __name__ == '__main__':
    start = time.time()
    all_tasks = []
    # difficulty_choice = get_user_choice(list(difficulty) + ['Random Choice'], 'Select difficulty:')
    # tag_choice = get_user_choice(list(tags) + ['Random Choice'], 'Select tag:')
    difficulty_choice = 'Easy'
    tag_choice = 'Dynamic Recursion'
    chosen_difficulty = difficulty[difficulty_choice]
    available_tags = tags[tag_choice]
    for url in urls.values():
        parse_url = url['url'] + url['postfix']
        own_links = [parse_url + slugify_tag(tag, url) for tag in available_tags if url['url_filter'](parse_url + slugify_tag(tag, url))]
        for link in own_links:
            url['parse_function'](link, chosen_difficulty, all_tasks)
    random_tasks = get_random_tasks(5, all_tasks)
    for task in random_tasks:
        print(task)

    print(time.time() - start)













# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
#
# browser = webdriver.Chrome()
# url = 'https://leetcode.com/'
# postfix = 'tag/dynamic-programming'
#
#
# browser.get(url+postfix)
# time.sleep(4)
#
#
# def filter_by_difficulty(cell, difficulty):
#     new_cell = cell.find('span', class_='label')
#     if new_cell and new_cell.text == difficulty:
#         return True
#     return False
#
#
# soup = BeautifulSoup(browser.page_source, 'lxml')
# task_blocks = soup.find_all('tr')
# tasks = []
# for task in task_blocks:
#     if task.find('i', class_="fa-lock") is None and filter_by_difficulty(task, 'Easy'):
#         link = task.find('div', class_="title-cell__ZGos")
#         if link:
#             new_task = link.find('a').get('href')
#             tasks.append(url + new_task[1:])
#
#
# browser.quit()
#
# [print(task) for task in tasks]


# filter_parameters = {'difficulty level': {'class': 'inner-small-hex', 'tag': 'span'},
#                      'theme tag': {'class': 'keyword-tag', 'tag': 'a'}}
#
# url = 'https://www.codewars.com/kata/search/python?q=&beta=false&order_by=sort_date%20desc'
# response = requests.get(url)
#
#
# def get_user_choice(variants, title='Select an option:'):
#     print(title)
#     for i, variant in enumerate(variants):
#         print(f'{i} - {variant}')
#     ans = input()
#
#     while not ans.isdigit() or not (int(ans) in range(len(variants))):
#         print(f'Enter digit in range 0-{len(variants) - 1}:')
#         ans = input()
#
#     if variants[int(ans)] == 'random':
#         return random.choice(variants[:-1])
#
#     return variants[int(ans)]
#
#
# def get_one_task(div, tasks):
#     link = div.find('a', href=re.compile(r'python$'))
#     href = link['href']
#     tasks.append(href)
#
#
# def get_all_tasks(task_divs):
#     tasks = []
#     for div in task_divs:
#         get_one_task(div, tasks)
#     return tasks
#
#
# def get_possible_filters(soup, filter_params):
#     filters = set()
#     filter_divs = soup.find_all('div', class_=filter_params['class'])
#     for div in filter_divs:
#         new_filter = div.find(filter_params['tag']).text
#         filters.add(new_filter)
#     return sorted(filters)
#
#
# def get_tasks_by_filter(task_divs, filter_params, filter_choice):
#     tasks = []
#     for div in task_divs:
#         link = div.find(filter_params['tag'], string=filter_choice)
#         if link:
#             get_one_task(div, tasks)
#     return tasks
#
#
# def get_tasks_by_codewars(soup):
#     task_divs = soup.find_all('div', class_='list-item-kata')
#     main_filters = sorted(filter_parameters) + ['all tasks']
#     question = 'Do you wanna filter tasks?'
#     user_filter_choice = get_user_choice(main_filters, question)
#
#     if user_filter_choice in filter_parameters:
#         filter_params = filter_parameters[user_filter_choice]
#         possible_filters = get_possible_filters(soup, filter_params)
#         local_filter_choice = get_user_choice(possible_filters + ['random'])
#         print(local_filter_choice)
#         tasks = get_tasks_by_filter(task_divs, filter_params, local_filter_choice)
#     else:
#         tasks = get_all_tasks(task_divs)
#
#     return tasks
#
#
# if response.status_code == 200:
#     soup = BeautifulSoup(response.content, 'html.parser')
#     tasks = get_tasks_by_codewars(soup)
#     for i, task in enumerate(tasks, 1):
#         print(f'{i}. codewars.com{task}')
# else:
#     print('Response Error: ', response.status_code)


# url = 'https://leetcode.com/'
# param = 'problemset/'
#
# payload = "{\"sent_at\":\"2024-03-07T12:54:29.393Z\",\"sdk\":{\"name\":\"sentry.javascript.nextjs\",\"version\":\"7.51.2\"}}\n{\"type\":\"session\"}\n{\"sid\":\"24ac7a8498ac4d6b8c474dfc11570770\",\"init\":true,\"started\":\"2024-03-07T12:54:29.392Z\",\"timestamp\":\"2024-03-07T12:54:29.392Z\",\"status\":\"ok\",\"errors\":0,\"attrs\":{\"release\":\"6e3eb75f\",\"environment\":\"production\",\"user_agent\":\"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36\"}}&{\"query\":\"\\n    query globalData {\\n  userStatus {\\n    userId\\n    isSignedIn\\n    isMockUser\\n    isPremium\\n    isVerified\\n    username\\n    avatar\\n    isAdmin\\n    isSuperuser\\n    permissions\\n    isTranslator\\n    activeSessionId\\n    checkedInToday\\n    completedFeatureGuides\\n    notificationStatus {\\n      lastModified\\n      numUnread\\n    }\\n  }\\n}\\n    \",\"variables\":{},\"operationName\":\"globalData\"}&{\"query\":\"\\n    query siteAnnouncements {\\n  siteAnnouncements {\\n    title\\n    content\\n    blacklistUrls\\n    whitelistUrls\\n    navbarItem\\n  }\\n}\\n    \",\"variables\":{},\"operationName\":\"siteAnnouncements\"}&{\"query\":\"\\n    query GetProblemSetStudyPlanAds {\\n  studyPlansV2AdQuestionPage {\\n    cover\\n    highlight\\n    name\\n    onGoing\\n    premiumOnly\\n    questionNum\\n    slug\\n  }\\n}\\n    \",\"variables\":{},\"operationName\":\"GetProblemSetStudyPlanAds\"}&{\"query\":\"\\n    query questionCompanyTags {\\n  companyTags {\\n    name\\n    slug\\n    questionCount\\n  }\\n}\\n    \",\"variables\":{},\"operationName\":\"questionCompanyTags\"}&{\"query\":\"\\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\\n  problemsetQuestionList: questionList(\\n    categorySlug: $categorySlug\\n    limit: $limit\\n    skip: $skip\\n    filters: $filters\\n  ) {\\n    total: totalNum\\n    questions: data {\\n      acRate\\n      difficulty\\n      freqBar\\n      frontendQuestionId: questionFrontendId\\n      isFavor\\n      paidOnly: isPaidOnly\\n      status\\n      title\\n      titleSlug\\n      topicTags {\\n        name\\n        id\\n        slug\\n      }\\n      hasSolution\\n      hasVideoSolution\\n    }\\n  }\\n}\\n    \",\"variables\":{\"categorySlug\":\"all-code-essentials\",\"skip\":0,\"limit\":50,\"filters\":{}},\"operationName\":\"problemsetQuestionList\"}&{\"query\":\"\\n    query currentTimestamp {\\n  currentTimestamp\\n}\\n    \",\"variables\":{},\"operationName\":\"currentTimestamp\"}&{\"query\":\"\\n    query questionOfToday {\\n  activeDailyCodingChallengeQuestion {\\n    date\\n    userStatus\\n    link\\n    question {\\n      acRate\\n      difficulty\\n      freqBar\\n      frontendQuestionId: questionFrontendId\\n      isFavor\\n      paidOnly: isPaidOnly\\n      status\\n      title\\n      titleSlug\\n      hasVideoSolution\\n      hasSolution\\n      topicTags {\\n        name\\n        id\\n        slug\\n      }\\n    }\\n  }\\n}\\n    \",\"variables\":{},\"operationName\":\"questionOfToday\"}&{\"query\":\"\\n    query codingChallengeMedal($year: Int!, $month: Int!) {\\n  dailyChallengeMedal(year: $year, month: $month) {\\n    name\\n    config {\\n      icon\\n    }\\n  }\\n}\\n    \",\"variables\":{\"year\":2024,\"month\":3},\"operationName\":\"codingChallengeMedal\"}&{\"query\":\"\\n    query GetMyStudyPlan($progressType: PlanUserProgressTypeEnum!, $offset: Int!, $limit: Int!) {\\n  studyPlanV2UserProgresses(\\n    progressType: $progressType\\n    offset: $offset\\n    limit: $limit\\n  ) {\\n    hasMore\\n    total\\n    planUserProgresses {\\n      nextQuestionInfo {\\n        inPremiumSubgroup\\n        nextQuestion {\\n          id\\n          questionFrontendId\\n          title\\n          titleSlug\\n          translatedTitle\\n        }\\n      }\\n      nextQuestionInfo {\\n        inPremiumSubgroup\\n        nextQuestion {\\n          id\\n          questionFrontendId\\n          title\\n          titleSlug\\n          translatedTitle\\n        }\\n      }\\n      quittedAt\\n      startedAt\\n      plan {\\n        questionNum\\n        slug\\n        premiumOnly\\n        name\\n        onGoing\\n        highlight\\n        cover\\n      }\\n      latestSubmissionAt\\n      id\\n      allCompletedAt\\n      finishedQuestionNum\\n    }\\n  }\\n}\\n    \",\"variables\":{\"offset\":0,\"limit\":3,\"progressType\":\"ON_GOING\"},\"operationName\":\"GetMyStudyPlan\"}&{\"query\":\"\\n    query dailyCodingQuestionRecords($year: Int!, $month: Int!) {\\n  dailyCodingChallengeV2(year: $year, month: $month) {\\n    challenges {\\n      date\\n      userStatus\\n      link\\n      question {\\n        questionFrontendId\\n        title\\n        titleSlug\\n      }\\n    }\\n    weeklyChallenges {\\n      date\\n      userStatus\\n      link\\n      question {\\n        questionFrontendId\\n        title\\n        titleSlug\\n        isPaidOnly\\n      }\\n    }\\n  }\\n}\\n    \",\"variables\":{\"year\":2024,\"month\":3},\"operationName\":\"dailyCodingQuestionRecords\"}&{\"query\":\"\\n    query upcOnboardingStatus {\\n  didCompleteUpc\\n  user {\\n    joinedTimestamp\\n  }\\n}\\n    \",\"operationName\":\"upcOnboardingStatus\"}&event=%7B%22event_name%22%3A%22problemset_page_exposure%22%2C%22event_data%22%3A%7B%7D%7D&6ðD\næ\u0005Æ\bÀS\u0002\u0018\u0004Àì\u00030\u0003\u0000\u000bFÆ\u0000±§±X\u0004À\u0007\u001eJ\u0014J\\@(\nÀ3\n\u0001³UØ\u00004`\u00038Ã\u000e\u0004¸\n\u0014©\\¡\u000e(óQÄ\u001c¼\u0010uä\u001a4Å*ñ\u0016\u0000\u000b\u001bI\u0000\u0014\u00018\u0007±Ëa\u0000[1\u0000\bðø\u0001@F°\u0006\u0011q@B¶´\u0000r@\u00072\u0016´ñBÅf£âÃCâU\u0015\u0000¶¶µ\u0011Dñ\f @\u0003¦kI,\u0007¥wró\u0011\n²pÄ\u0000\u0005ð\u0005Ò\u0000\u0000&6ðD\næ\u0005Æ\bÀS\u0002\u0018\u0004Àì\u00030\u0003\u0000\u000bFÆ\u0000±§±X\u0004À\u0007\u001eJ\u0014J\\@(\nÀ3\n\u0001³UØ\u00004`\u00038Ã\u000e\u0004¸\n\u0014©\\¡\u000e(óQÄ\u001c¼\u0010uä\u001a4Å*ñ\u0016\u0000\u000b¤Âc¬\u0005²´æ\u001c4Y[SË\u001a8\\h¢\u0000\u000e®ÐîÞ¾þ¡\u0000ô!\u0000N\u0000ö8\u00006\bb\b¶¢\u0000v©\u0019Ù¹ù\u0000ú!H\u0000æ\b\b\u0000\u001e!ib\u0010)\bV(Ùùi(\b\u0000t\u0003Î\u0000¾\u0000º@\u0000&6ðD\næ\u0005Æ\bÀS\u0002\u0018\u0004Àì\u00030\u0003\u0000\u000bFÆ\u0000±§±X\u0004À\u0007\u001eJ\u0014J\\@(\nÀ3\n\u0001³UØ\u00004`\u00038Ã\u000e\u0004¸\n\u0014©\\¡\u000e(óQÄ\u001c¼\u0010uä\u001a4Å*ñ\u0016\u0000\u000b¤Âc¬\u0005²´æ\u001c4Y[SË\u001a8\\4¢\u0000\u000e®ÐîÞ¾þ!\u0000ôÁ\u0000N\u0000ö8\u00006\bb\b¶¢\u0000v)éY9y\u0000ú¨\u0015\b\u0000\u001eÁ©b\u0010É\bV\u0000nHÉ0à%Ù¹ÖU(\u0015\rb\u0000Öc©E°V½e\u0003C\u0015\u0005H­°\u00002\u0000\u0000Â;x\u0000Ê\u0000\"`\u0000¾¢(Yy©(\b\u0000t·Î§\u0000º@\u0000&6ðD\næ\u0005Æ\bÀS\u0002\u0018\u0004Àì\u00030\u0003\u0000\u000bFÆ\u0000±§±X\u0004À\u0007\u001eJ\u0014J\\@(\nÀ3\n\u0001³UØ\u00004`\u00038Ã\u000e\u0004¸\n\u0014©\\¡\u000e(óQÄ\u001c¼\u0010uä\u001a4Å*ñ\u0016\u0000\u000b¤Âc¬\u0005²´æ\u001c4Y[SË\u001a8\\¬¢\u0000\u000e®ÐîÞ¾þ¡\u0000ô!\u0000N\u0000ö8\u00006\bb\b¶¢\u0000v©\u0019Ù¹ù\u0000ú¨\b\u0000\u001e!ib\u0010)\bV\u0000nH)0à¥Y9yÖÕ(b\u0000ÖãiÅ°V}åÃHm°\u00002\bù\u0000Bii\u0000Ö\u0000\u0004xÇ\u0000Ö\b)íã\b\u0000îÇ\u0000Â)Hb\u0000\u0016Çi-y§Ç\u0000\u0002º_¬à\u0002úPl¾Gâ@\u0000è~à.\u0000\u0000&6ðD\næ\u0005Æ\bÀS\u0002\u0018\u0004Àì\u00030\u0003\u0000\u000bFÆ\u0000±§±X\u0004À\u0007\u001eJ\u0014J\\@(\nÀ3\n\u0001³UØ\u00004`\u00038Ã\u000e\u0004¸\n\u0014©\\¡\u000e(óQÄ\u001c¼\u0010uä\u001a4Å*ñ\u0016\u0000\u000b¤Âc¬\u0005²´æ\u001c4Y[SË\u001a8\\\\p¢\u0000\u000e®ÐîÞ¾þ\\J¡\u0000ô!\u0000N\u0000ö8\u00006\bb\b¶¢\u0000v©\u0019Ù¹ù\u0000ú¨\b\u0000\u001e!ib\u0010)\bV\u0000nH)0à¥Y9yÖÕ(b\u0000ÖãiÅ°V}åÃHm°\u0000*i!\u0000\u0004\u0000Ö\b)íã\b\u0000î»\u0000\u0010\b\u000eÓb»\u0000BH'`\u0000¾¢(Ù|¡\r\"@\u0000éÎo\u0017H\u0000\u0000&en=page_view&_ee=1&up.is_premium=false\r\nen=problemset_page_exposure&_ee=1\r\nen=problemset_ad_exposure&_ee=1&ep.event_param_1=problemset_ad_position%3A%20&ep.event_param_2=problemset_ad_name%3A%20LICC-SD\r\nen=problemset_ad_exposure&_ee=1&ep.event_param_1=problemset_ad_position%3A%20&ep.event_param_2=problemset_ad_name%3A%20LeetBook%20-%20Interview%20Crash%20course%20-%20Problem\r\nen=problemset_ad_exposure&_ee=1&ep.event_param_1=problemset_ad_position%3A%20&ep.event_param_2=problemset_ad_name%3A%20Top%20Interview%20Questions%20Banner&bel.6;e,'fcp,mv,3;5,'net-etype,'4g;6,'net-rtt,250.;6,'net-dlink,2.1;e,'fp,mv,3;5,1,2;6,3,250.;6,4,2.1;e,'load,u1,3;5,1,2;6,3,250.;6,4,2.1&bel.7;2,,13b,ep,,,'GET,5k,'leetcode.com:443,'/api/banner/problemset_primary/,,,1,'0,!!!;2,,13n,ef,,,0,5k,1,'/problems/api/favorites/,,,1,3,!!!;2,,146,g0,,,0,5k,1,'/problems/api/card-info/,,,1,3,!!!;2,3,12z,ic,,,'POST,5k,1,'/graphql/,bj,8n,,3,!!!;5,'operationName,'globalData;5,'operationType,'query;5,'operationFramework,'GraphQL;2,3,13x,hl,,,6,5k,1,7,fs,1ee,,3,!!!;5,8,'dailyCodingQuestionRecords;5,a,b;5,c,d;2,3,13d,i6,,,6,5k,1,7,6x,148,,3,!!!;5,8,'GetProblemSetStudyPlanAds;5,a,b;5,c,d;2,3,13r,hu,,,6,5k,1,7,76,3w,,3,!!!;5,8,'codingChallengeMedal;5,a,b;5,c,d;2,3,13p,hy,,,6,5k,1,7,dq,fq,,3,!!!;5,8,'questionOfToday;5,a,b;5,c,d;2,3,143,hm,,,6,5k,1,7,42,19,,3,!!!;5,8,'upcOnboardingStatus;5,a,b;5,c,d;2,,132,11g,,,0,5k,'leetcode.cn:443,'/api/is_china_ip/,,o,1,3,!!!;2,3,137,11c,,,6,5k,1,7,5t,x,,3,!!!;5,8,'siteAnnouncements;5,a,b;5,c,d;2,,140,10s,,,0,5k,1,'/api/banner/problemset/,,2,1,3,!!!&{}\n{\"type\":\"client_report\"}\n{\"timestamp\":1709816131.742,\"discarded_events\":[{\"reason\":\"sample_rate\",\"category\":\"transaction\",\"quantity\":1}]}&bel.6;e,'lcp,1n8,8;6,'size,36450.;5,'eid;5,'elUrl,'https://assets.leetcode.com/users/images/49479bba-73b3-45d2-9272-99e773d784b2_1687290663.3168745.jpeg;5,'elTag,'IMG;5,'net-etype,'4g;6,'net-rtt,250.;6,'net-dlink,2.1;6,'cls,0.0007964722800431445;e,'pageHide,1cud,4;5,7,8;6,9,250.;6,a,2.1;6,b,0.0007964722800431445&{\"sm\":[{\"params\":{\"name\":\"Generic/LoaderType/spa/Detected\"},\"stats\":{\"c\":1}},{\"params\":{\"name\":\"Generic/DistMethod/CDN/Detected\"},\"stats\":{\"c\":1}},{\"params\":{\"name\":\"Generic/Runtime/Browser/Detected\"},\"stats\":{\"c\":1}}]}&{\"query\":\"\\n    query currentTimestamp {\\n  currentTimestamp\\n}\\n    \",\"variables\":{},\"operationName\":\"currentTimestamp\"}&{\"query\":\"\\n    query currentTimestamp {\\n  currentTimestamp\\n}\\n    \",\"variables\":{},\"operationName\":\"currentTimestamp\"}"
#
# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'ru-RU,ru;q=0.9',
#     'cache-control': 'max-age=0',
#     'cookie': 'INGRESSCOOKIE=bf39a46c0bd7edb933cdd533a5991793|8e0876c7c1464cc0ac96bc2edceabd27; csrftoken=NZDgOTR4uH3zNARBK1EgnVn3ql9Ph8il7vrR6QMU4bSiPVNIZDeabLdVdzMNdHf5; _gid=GA1.2.71519846.1709810884; gr_user_id=1ead7f0b-7c47-4028-aca7-a249d53d6834; __stripe_mid=24bf0f1e-e922-4929-947e-8d3da08dce011fc4f3; __cf_bm=9I1ZXoTFy4YGhYq3nyQrAVrlK5Xr7zm43YEuTbj.34g-1709816022-1.0.1.1-7g1KlzE9wgG9URX.rzrgIEW8XIuieB9AjK79Q5TTjimtv.oq7CjAByQHM_5s1IOMq3mp0W6hekHFtaTOVH8PFA; 87b5a3c3f1a55520_gr_session_id=d7a2be0b-7c22-4c5d-8ba9-b6e56ae77426; 87b5a3c3f1a55520_gr_session_id_sent_vst=d7a2be0b-7c22-4c5d-8ba9-b6e56ae77426; _gat=1; _ga=GA1.1.336053973.1709810884; _ga_CDRWKZTDEX=GS1.1.1709816024.2.1.1709816047.37.0.0; __cf_bm=mVgnigUiIztCFsVFSUYkVb7LWro.ZXg7NuOIDJqWTzY-1709822477-1.0.1.1-Icb5EbsdHMaR2ZcpFzqtNvruYpIETEDiiTFxV4gBgGt5WjfFYVdN39_ZcZ6eL_fHEE1ssn8gH0QVmL4W7WAKWQ',
#     'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
#     'Referer': 'https://leetcode.com/problemset/',
#     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
#     'referer': 'https://leetcode.com/_next/static/css/9b0ee8287b505155.css',
#     'content-type': 'text/plain;charset=UTF-8',
#     'Accept': '*/*',
#     'Accept-Language': 'ru-RU,ru;q=0.9',
#     'Connection': 'keep-alive',
#     'uuuserid': 'f44e75d3cc2e3b63d02ebf72cd1a5700'
# }
#
# response = requests.request("GET", url + param, headers=headers, data=payload)
#
# if response.status_code == 200:
#     time.sleep(4)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     tags = []
#     tag_divs = soup.find_all('div', class_='group m-[10px] flex items-center')
#
#     # tag_divs = tag_divs[:28]
#     for div in tag_divs:
#         link = div.find('span', class_='whitespace-nowrap')
#         tags.append(link.string)
#     # current_tag = random.choice(tags)
#     # current_tag = 'dynamic-programming'
#     # print(current_tag)
#     # param = f'tag/{slugify(current_tag)}'
#     # time.sleep(0.5)
# else:
#     tags = []
#     print('Error', response.status_code)
# url = response = None

# if url is not None:
#     response = requests.get(url + param, headers=headers, data=payload)
#
# if response and response.status_code == 200:
#     soup = BeautifulSoup(response.content, 'lxml')
#     print(soup)
#     task_blocks = soup.find_all('tr')
#     task_blocks = soup.find_all('a')
#     for task in task_blocks:
#         print(task)
#         if task.find('i', class_="fa-lock"):
#             print('ok')
#             #task.find('div', class_="title-cell__ZGos").find('a').get('href')
# else:
#     print('Error', response.status_code)
