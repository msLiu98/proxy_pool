from .utils import get_page
from pyquery import PyQuery as pq
import re
import time
from lxml import etree


class ProxyMetaclass(type):
    """
        元类，在FreeProxyGetter类中加入
        __CrawlFunc__和__CrawlFuncCount__
        两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):

    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            # print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    # 非实时更新
    def crawl_ip3366(self, page_count=5):
        start_url = 'http://www.ip3366.net/free/?stype=1&page={}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            time.sleep(2)
            html = get_page(url)
            if html:
                doc = etree.HTML(html)
                ips = doc.xpath('//div[@id="list"]/table//tr/td[1]/text()')
                ports = doc.xpath('//div[@id="list"]/table//tr/td[2]/text()')
                for ip, port in set(tuple(zip(ips, ports))):
                    yield ':'.join([ip, port])

    def crawl_kuaidaili(self, page_count=6):
        base_url = 'https://www.kuaidaili.com/free/inha/{}/'
        start_urls = [base_url.format(page) for page in range(1, page_count + 1)]
        for url in start_urls:
            # 国内高匿代理
            time.sleep(1)
            html = get_page(url)
            ip_adress = re.compile(
                '<td data-title="IP">(.*)</td>\s*<td data-title="PORT">(\w+)</td>'
            )
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_daili66(self, page_count=10):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            time.sleep(1)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_xila(self):
        start_url = 'http://www.xiladaili.com/'
        html = get_page(start_url)
        ip_adress = re.compile(
            '<td>(.*)</td>\s*<td>高匿名ip代理</td>'
        )
        # \s * 匹配空格，起到换行作用
        re_ip_adress = ip_adress.findall(str(html))
        for ip in re_ip_adress:
            yield ip
