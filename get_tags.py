import requests
from bs4 import BeautifulSoup
import time

urls = {'lc': {'name': 'leetcode',
               'url': 'https://leetcode.com/',
               'postfix': 'problemset/',
               'payload': True},
        'cw': {'name': 'codewars',
               'url': 'https://www.codewars.com/',
               'postfix': 'kata/search/python'}}

payload = "{\"sent_at\":\"2024-03-07T12:54:29.393Z\",\"sdk\":{\"name\":\"sentry.javascript.nextjs\",\"version\":\"7.51.2\"}}\n{\"type\":\"session\"}\n{\"sid\":\"24ac7a8498ac4d6b8c474dfc11570770\",\"init\":true,\"started\":\"2024-03-07T12:54:29.392Z\",\"timestamp\":\"2024-03-07T12:54:29.392Z\",\"status\":\"ok\",\"errors\":0,\"attrs\":{\"release\":\"6e3eb75f\",\"environment\":\"production\",\"user_agent\":\"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36\"}}&{\"query\":\"\\n    query globalData {\\n  userStatus {\\n    userId\\n    isSignedIn\\n    isMockUser\\n    isPremium\\n    isVerified\\n    username\\n    avatar\\n    isAdmin\\n    isSuperuser\\n    permissions\\n    isTranslator\\n    activeSessionId\\n    checkedInToday\\n    completedFeatureGuides\\n    notificationStatus {\\n      lastModified\\n      numUnread\\n    }\\n  }\\n}\\n    \",\"variables\":{},\"operationName\":\"globalData\"}&{\"query\":\"\\n    query siteAnnouncements {\\n  siteAnnouncements {\\n    title\\n    content\\n    blacklistUrls\\n    whitelistUrls\\n    navbarItem\\n  }\\n}\\n    \",\"variables\":{},\"operationName\":\"siteAnnouncements\"}&{\"query\":\"\\n    query GetProblemSetStudyPlanAds {\\n  studyPlansV2AdQuestionPage {\\n    cover\\n    highlight\\n    name\\n    onGoing\\n    premiumOnly\\n    questionNum\\n    slug\\n  }\\n}\\n    \",\"variables\":{},\"operationName\":\"GetProblemSetStudyPlanAds\"}&{\"query\":\"\\n    query questionCompanyTags {\\n  companyTags {\\n    name\\n    slug\\n    questionCount\\n  }\\n}\\n    \",\"variables\":{},\"operationName\":\"questionCompanyTags\"}&{\"query\":\"\\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\\n  problemsetQuestionList: questionList(\\n    categorySlug: $categorySlug\\n    limit: $limit\\n    skip: $skip\\n    filters: $filters\\n  ) {\\n    total: totalNum\\n    questions: data {\\n      acRate\\n      difficulty\\n      freqBar\\n      frontendQuestionId: questionFrontendId\\n      isFavor\\n      paidOnly: isPaidOnly\\n      status\\n      title\\n      titleSlug\\n      topicTags {\\n        name\\n        id\\n        slug\\n      }\\n      hasSolution\\n      hasVideoSolution\\n    }\\n  }\\n}\\n    \",\"variables\":{\"categorySlug\":\"all-code-essentials\",\"skip\":0,\"limit\":50,\"filters\":{}},\"operationName\":\"problemsetQuestionList\"}&{\"query\":\"\\n    query currentTimestamp {\\n  currentTimestamp\\n}\\n    \",\"variables\":{},\"operationName\":\"currentTimestamp\"}&{\"query\":\"\\n    query questionOfToday {\\n  activeDailyCodingChallengeQuestion {\\n    date\\n    userStatus\\n    link\\n    question {\\n      acRate\\n      difficulty\\n      freqBar\\n      frontendQuestionId: questionFrontendId\\n      isFavor\\n      paidOnly: isPaidOnly\\n      status\\n      title\\n      titleSlug\\n      hasVideoSolution\\n      hasSolution\\n      topicTags {\\n        name\\n        id\\n        slug\\n      }\\n    }\\n  }\\n}\\n    \",\"variables\":{},\"operationName\":\"questionOfToday\"}&{\"query\":\"\\n    query codingChallengeMedal($year: Int!, $month: Int!) {\\n  dailyChallengeMedal(year: $year, month: $month) {\\n    name\\n    config {\\n      icon\\n    }\\n  }\\n}\\n    \",\"variables\":{\"year\":2024,\"month\":3},\"operationName\":\"codingChallengeMedal\"}&{\"query\":\"\\n    query GetMyStudyPlan($progressType: PlanUserProgressTypeEnum!, $offset: Int!, $limit: Int!) {\\n  studyPlanV2UserProgresses(\\n    progressType: $progressType\\n    offset: $offset\\n    limit: $limit\\n  ) {\\n    hasMore\\n    total\\n    planUserProgresses {\\n      nextQuestionInfo {\\n        inPremiumSubgroup\\n        nextQuestion {\\n          id\\n          questionFrontendId\\n          title\\n          titleSlug\\n          translatedTitle\\n        }\\n      }\\n      nextQuestionInfo {\\n        inPremiumSubgroup\\n        nextQuestion {\\n          id\\n          questionFrontendId\\n          title\\n          titleSlug\\n          translatedTitle\\n        }\\n      }\\n      quittedAt\\n      startedAt\\n      plan {\\n        questionNum\\n        slug\\n        premiumOnly\\n        name\\n        onGoing\\n        highlight\\n        cover\\n      }\\n      latestSubmissionAt\\n      id\\n      allCompletedAt\\n      finishedQuestionNum\\n    }\\n  }\\n}\\n    \",\"variables\":{\"offset\":0,\"limit\":3,\"progressType\":\"ON_GOING\"},\"operationName\":\"GetMyStudyPlan\"}&{\"query\":\"\\n    query dailyCodingQuestionRecords($year: Int!, $month: Int!) {\\n  dailyCodingChallengeV2(year: $year, month: $month) {\\n    challenges {\\n      date\\n      userStatus\\n      link\\n      question {\\n        questionFrontendId\\n        title\\n        titleSlug\\n      }\\n    }\\n    weeklyChallenges {\\n      date\\n      userStatus\\n      link\\n      question {\\n        questionFrontendId\\n        title\\n        titleSlug\\n        isPaidOnly\\n      }\\n    }\\n  }\\n}\\n    \",\"variables\":{\"year\":2024,\"month\":3},\"operationName\":\"dailyCodingQuestionRecords\"}&{\"query\":\"\\n    query upcOnboardingStatus {\\n  didCompleteUpc\\n  user {\\n    joinedTimestamp\\n  }\\n}\\n    \",\"operationName\":\"upcOnboardingStatus\"}&event=%7B%22event_name%22%3A%22problemset_page_exposure%22%2C%22event_data%22%3A%7B%7D%7D&6ðD\næ\u0005Æ\bÀS\u0002\u0018\u0004Àì\u00030\u0003\u0000\u000bFÆ\u0000±§±X\u0004À\u0007\u001eJ\u0014J\\@(\nÀ3\n\u0001³UØ\u00004`\u00038Ã\u000e\u0004¸\n\u0014©\\¡\u000e(óQÄ\u001c¼\u0010uä\u001a4Å*ñ\u0016\u0000\u000b\u001bI\u0000\u0014\u00018\u0007±Ëa\u0000[1\u0000\bðø\u0001@F°\u0006\u0011q@B¶´\u0000r@\u00072\u0016´ñBÅf£âÃCâU\u0015\u0000¶¶µ\u0011Dñ\f @\u0003¦kI,\u0007¥wró\u0011\n²pÄ\u0000\u0005ð\u0005Ò\u0000\u0000&6ðD\næ\u0005Æ\bÀS\u0002\u0018\u0004Àì\u00030\u0003\u0000\u000bFÆ\u0000±§±X\u0004À\u0007\u001eJ\u0014J\\@(\nÀ3\n\u0001³UØ\u00004`\u00038Ã\u000e\u0004¸\n\u0014©\\¡\u000e(óQÄ\u001c¼\u0010uä\u001a4Å*ñ\u0016\u0000\u000b¤Âc¬\u0005²´æ\u001c4Y[SË\u001a8\\h¢\u0000\u000e®ÐîÞ¾þ¡\u0000ô!\u0000N\u0000ö8\u00006\bb\b¶¢\u0000v©\u0019Ù¹ù\u0000ú!H\u0000æ\b\b\u0000\u001e!ib\u0010)\bV(Ùùi(\b\u0000t\u0003Î\u0000¾\u0000º@\u0000&6ðD\næ\u0005Æ\bÀS\u0002\u0018\u0004Àì\u00030\u0003\u0000\u000bFÆ\u0000±§±X\u0004À\u0007\u001eJ\u0014J\\@(\nÀ3\n\u0001³UØ\u00004`\u00038Ã\u000e\u0004¸\n\u0014©\\¡\u000e(óQÄ\u001c¼\u0010uä\u001a4Å*ñ\u0016\u0000\u000b¤Âc¬\u0005²´æ\u001c4Y[SË\u001a8\\4¢\u0000\u000e®ÐîÞ¾þ!\u0000ôÁ\u0000N\u0000ö8\u00006\bb\b¶¢\u0000v)éY9y\u0000ú¨\u0015\b\u0000\u001eÁ©b\u0010É\bV\u0000nHÉ0à%Ù¹ÖU(\u0015\rb\u0000Öc©E°V½e\u0003C\u0015\u0005H­°\u00002\u0000\u0000Â;x\u0000Ê\u0000\"`\u0000¾¢(Yy©(\b\u0000t·Î§\u0000º@\u0000&6ðD\næ\u0005Æ\bÀS\u0002\u0018\u0004Àì\u00030\u0003\u0000\u000bFÆ\u0000±§±X\u0004À\u0007\u001eJ\u0014J\\@(\nÀ3\n\u0001³UØ\u00004`\u00038Ã\u000e\u0004¸\n\u0014©\\¡\u000e(óQÄ\u001c¼\u0010uä\u001a4Å*ñ\u0016\u0000\u000b¤Âc¬\u0005²´æ\u001c4Y[SË\u001a8\\¬¢\u0000\u000e®ÐîÞ¾þ¡\u0000ô!\u0000N\u0000ö8\u00006\bb\b¶¢\u0000v©\u0019Ù¹ù\u0000ú¨\b\u0000\u001e!ib\u0010)\bV\u0000nH)0à¥Y9yÖÕ(b\u0000ÖãiÅ°V}åÃHm°\u00002\bù\u0000Bii\u0000Ö\u0000\u0004xÇ\u0000Ö\b)íã\b\u0000îÇ\u0000Â)Hb\u0000\u0016Çi-y§Ç\u0000\u0002º_¬à\u0002úPl¾Gâ@\u0000è~à.\u0000\u0000&6ðD\næ\u0005Æ\bÀS\u0002\u0018\u0004Àì\u00030\u0003\u0000\u000bFÆ\u0000±§±X\u0004À\u0007\u001eJ\u0014J\\@(\nÀ3\n\u0001³UØ\u00004`\u00038Ã\u000e\u0004¸\n\u0014©\\¡\u000e(óQÄ\u001c¼\u0010uä\u001a4Å*ñ\u0016\u0000\u000b¤Âc¬\u0005²´æ\u001c4Y[SË\u001a8\\\\p¢\u0000\u000e®ÐîÞ¾þ\\J¡\u0000ô!\u0000N\u0000ö8\u00006\bb\b¶¢\u0000v©\u0019Ù¹ù\u0000ú¨\b\u0000\u001e!ib\u0010)\bV\u0000nH)0à¥Y9yÖÕ(b\u0000ÖãiÅ°V}åÃHm°\u0000*i!\u0000\u0004\u0000Ö\b)íã\b\u0000î»\u0000\u0010\b\u000eÓb»\u0000BH'`\u0000¾¢(Ù|¡\r\"@\u0000éÎo\u0017H\u0000\u0000&en=page_view&_ee=1&up.is_premium=false\r\nen=problemset_page_exposure&_ee=1\r\nen=problemset_ad_exposure&_ee=1&ep.event_param_1=problemset_ad_position%3A%20&ep.event_param_2=problemset_ad_name%3A%20LICC-SD\r\nen=problemset_ad_exposure&_ee=1&ep.event_param_1=problemset_ad_position%3A%20&ep.event_param_2=problemset_ad_name%3A%20LeetBook%20-%20Interview%20Crash%20course%20-%20Problem\r\nen=problemset_ad_exposure&_ee=1&ep.event_param_1=problemset_ad_position%3A%20&ep.event_param_2=problemset_ad_name%3A%20Top%20Interview%20Questions%20Banner&bel.6;e,'fcp,mv,3;5,'net-etype,'4g;6,'net-rtt,250.;6,'net-dlink,2.1;e,'fp,mv,3;5,1,2;6,3,250.;6,4,2.1;e,'load,u1,3;5,1,2;6,3,250.;6,4,2.1&bel.7;2,,13b,ep,,,'GET,5k,'leetcode.com:443,'/api/banner/problemset_primary/,,,1,'0,!!!;2,,13n,ef,,,0,5k,1,'/problems/api/favorites/,,,1,3,!!!;2,,146,g0,,,0,5k,1,'/problems/api/card-info/,,,1,3,!!!;2,3,12z,ic,,,'POST,5k,1,'/graphql/,bj,8n,,3,!!!;5,'operationName,'globalData;5,'operationType,'query;5,'operationFramework,'GraphQL;2,3,13x,hl,,,6,5k,1,7,fs,1ee,,3,!!!;5,8,'dailyCodingQuestionRecords;5,a,b;5,c,d;2,3,13d,i6,,,6,5k,1,7,6x,148,,3,!!!;5,8,'GetProblemSetStudyPlanAds;5,a,b;5,c,d;2,3,13r,hu,,,6,5k,1,7,76,3w,,3,!!!;5,8,'codingChallengeMedal;5,a,b;5,c,d;2,3,13p,hy,,,6,5k,1,7,dq,fq,,3,!!!;5,8,'questionOfToday;5,a,b;5,c,d;2,3,143,hm,,,6,5k,1,7,42,19,,3,!!!;5,8,'upcOnboardingStatus;5,a,b;5,c,d;2,,132,11g,,,0,5k,'leetcode.cn:443,'/api/is_china_ip/,,o,1,3,!!!;2,3,137,11c,,,6,5k,1,7,5t,x,,3,!!!;5,8,'siteAnnouncements;5,a,b;5,c,d;2,,140,10s,,,0,5k,1,'/api/banner/problemset/,,2,1,3,!!!&{}\n{\"type\":\"client_report\"}\n{\"timestamp\":1709816131.742,\"discarded_events\":[{\"reason\":\"sample_rate\",\"category\":\"transaction\",\"quantity\":1}]}&bel.6;e,'lcp,1n8,8;6,'size,36450.;5,'eid;5,'elUrl,'https://assets.leetcode.com/users/images/49479bba-73b3-45d2-9272-99e773d784b2_1687290663.3168745.jpeg;5,'elTag,'IMG;5,'net-etype,'4g;6,'net-rtt,250.;6,'net-dlink,2.1;6,'cls,0.0007964722800431445;e,'pageHide,1cud,4;5,7,8;6,9,250.;6,a,2.1;6,b,0.0007964722800431445&{\"sm\":[{\"params\":{\"name\":\"Generic/LoaderType/spa/Detected\"},\"stats\":{\"c\":1}},{\"params\":{\"name\":\"Generic/DistMethod/CDN/Detected\"},\"stats\":{\"c\":1}},{\"params\":{\"name\":\"Generic/Runtime/Browser/Detected\"},\"stats\":{\"c\":1}}]}&{\"query\":\"\\n    query currentTimestamp {\\n  currentTimestamp\\n}\\n    \",\"variables\":{},\"operationName\":\"currentTimestamp\"}&{\"query\":\"\\n    query currentTimestamp {\\n  currentTimestamp\\n}\\n    \",\"variables\":{},\"operationName\":\"currentTimestamp\"}"

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'INGRESSCOOKIE=bf39a46c0bd7edb933cdd533a5991793|8e0876c7c1464cc0ac96bc2edceabd27; csrftoken=NZDgOTR4uH3zNARBK1EgnVn3ql9Ph8il7vrR6QMU4bSiPVNIZDeabLdVdzMNdHf5; _gid=GA1.2.71519846.1709810884; gr_user_id=1ead7f0b-7c47-4028-aca7-a249d53d6834; __stripe_mid=24bf0f1e-e922-4929-947e-8d3da08dce011fc4f3; __cf_bm=9I1ZXoTFy4YGhYq3nyQrAVrlK5Xr7zm43YEuTbj.34g-1709816022-1.0.1.1-7g1KlzE9wgG9URX.rzrgIEW8XIuieB9AjK79Q5TTjimtv.oq7CjAByQHM_5s1IOMq3mp0W6hekHFtaTOVH8PFA; 87b5a3c3f1a55520_gr_session_id=d7a2be0b-7c22-4c5d-8ba9-b6e56ae77426; 87b5a3c3f1a55520_gr_session_id_sent_vst=d7a2be0b-7c22-4c5d-8ba9-b6e56ae77426; _gat=1; _ga=GA1.1.336053973.1709810884; _ga_CDRWKZTDEX=GS1.1.1709816024.2.1.1709816047.37.0.0; __cf_bm=mVgnigUiIztCFsVFSUYkVb7LWro.ZXg7NuOIDJqWTzY-1709822477-1.0.1.1-Icb5EbsdHMaR2ZcpFzqtNvruYpIETEDiiTFxV4gBgGt5WjfFYVdN39_ZcZ6eL_fHEE1ssn8gH0QVmL4W7WAKWQ',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    'Referer': 'https://leetcode.com/problemset/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    'referer': 'https://leetcode.com/_next/static/css/9b0ee8287b505155.css',
    'content-type': 'text/plain;charset=UTF-8',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Connection': 'keep-alive',
    'uuuserid': 'f44e75d3cc2e3b63d02ebf72cd1a5700'
}


def get_tags_from_response(response, params):
    soup = BeautifulSoup(response.content, 'lxml')
    tags = []
    if params['name'] == 'leetcode':
        tag_divs = soup.find_all('div', class_='group m-[10px] flex items-center')
        for div in tag_divs:
            link = div.find('span', class_='whitespace-nowrap')
            tags.append(link.string)
    else:
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
        if 'payload' in params:
            response = requests.get(params['url'] + params['postfix'], headers=heads, data=pay_data)
        else:
            response = requests.get(params['url'] + params['postfix'], headers=heads)
        time.sleep(0.5)
        if response.status_code == 200:
            tags = get_tags_from_response(response, params)
            write_tags_on_file(tags, params)
        else:
            print('Error', response.status_code)


if __name__ == '__main__':
    get_tags_by_urls(urls, headers, payload)
