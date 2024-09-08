import typing

from core.engine.base import SearchResult
import re
import requests
from lxml.html import etree


class Google:

    def get_google_url(self, keywords):
        keywords = keywords.strip('\n')
        google_url = re.sub(r'^', 'https://www.google.com/search?q=', keywords)
        google_url = re.sub(r'\s', '+', google_url)
        return google_url

    def search(self, keywords, site) -> typing.List[SearchResult]:
        keywords = f'"{keywords}" 插件 site:{site}'
        url = self.get_google_url(keywords)
        result: typing.List[SearchResult] = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'Accept-Encoding': 'gzip, deflate',
                   'cookie': 'c8_iyMaUnxNYECBuCtWvdH2HYvITFFnFnRULTMb8fQEAAICGSTB--aTyMAEAAISvFQ9mKv6nXQAAAO4BBgAhOxlRFwAAAA'
                             '7646771_24_24__24_'
                             'a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNzIzMzc1NTQ0NDI2MDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDIyMzE3OTYxMAogIGxvbmdpdHVkZV9lNzogMTE0MTc0MTQxMAp9CnJhZGl1czogMTM4ODkyNDAKcHJvdmVuYW5jZTogNgo='
                             '1'
                   }
        content = requests.get(url=url, timeout=5, headers=headers, verify=False)
        tree = etree.HTML(content.text)
        a_list = tree.xpath('//a')
        p_l = tree.xpath("/html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/span[not(@class)]")
        p_list, u_list, t_list = [], [], []
        for p in p_l:
            try:
                para = p.xpath("string(.)")
                p_list.append(para)
            except Exception as e:
                pass
        for a in a_list:
            try:
                h3 = a.xpath(".//h3/text()")[0]
                url = a.get('href')
                if h3:
                    u_list.append(url)
                    t_list.append(h3)
            except Exception as e:
                pass
        for u in u_list:
            i = u_list.index(u)
            if i > len(p_list)-1:
                pli = ""
            else:
                pli = p_list[i]
            result.append(SearchResult(url=u, title=t_list[i], summary=pli))
        return result


if __name__ == '__main__':
    google = Google()
    result = google.search("Towny", "spigotmc.org")
    print(result)
    for obj in result:
        print(obj.title, obj.url, obj.summary)
