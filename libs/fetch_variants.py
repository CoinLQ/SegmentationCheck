# coding: utf-8
import requests
from BeautifulSoup import BeautifulSoup

class VariantsFetcher:
    def __init__(self):
	pass
        # self.session = requests.Session()
        # url = 'http://hanzi.lqdzj.cn/user/sign-in/login'
        # r = self.session.get(url)
        # if r.status_code == 200:
        #     soup = BeautifulSoup(r.text)
        #     self.csrf = soup.find('input').get('value')

        # data = {
        #     '_csrf': self.csrf,
        #     'LoginForm[identity]': 'fetchvariant',
        #     'LoginForm[password]': 'fetchvariant',
        #     'LoginForm[rememberMe]': '1',
        # }
        # r = self.session.post(url, data)
        # self.is_login = ( u'ETag' in r.headers )
        # char =u'塡'
        # url = 'http://hanzi.lqdzj.cn/hanzi-dict/search?param=%s' % char.encode('utf-8')
        # r = self.session.get(url)
        # soup = BeautifulSoup(r.text)
        # self.soup = soup

    def fetch_variants(self, char):
        if not self.is_login:
            return None
        url = 'http://hanzi.lqdzj.cn/variant_detail?q=%s' % char.encode('utf-8')
        r = self.session.get(url)
        soup = BeautifulSoup(r.text)
        self.soup = soup
        lq_variant = soup.find(id='lq-variant')
        for link in lq_variant.findAll('a'):
            link['href'] = u'http://hanzi.lqdzj.cn' + link['href']
        for link in lq_variant.findAll('img'):
            link['src'] = u'http://hanzi.lqdzj.cn' + link['src']
        return lq_variant

fetcher = VariantsFetcher()

if __name__ == '__main__':
    lq_variant = fetcher.fetch_variants(u'塡')
    print lq_variant
