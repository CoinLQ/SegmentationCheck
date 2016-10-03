# coding: utf-8
import requests
from BeautifulSoup import BeautifulSoup

class VariantsFetcher:
    def __init__(self):
        self.session = requests.Session()
        url = 'http://hanzi.lqdzj.cn/user/sign-in/login'
        r = self.session.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text)
            self.csrf = soup.find('input').get('value')

        data = {
            '_csrf': self.csrf,
            'LoginForm[identity]': 'xianbu',
            'LoginForm[password]': 'xianbu123',
            'LoginForm[rememberMe]': '1',
        }
        r = self.session.post(url, data)
        self.is_login = ( u'ETag' in r.headers )

    def fetch_variants(self, char):
        if not self.is_login:
            return None
        url = 'http://hanzi.lqdzj.cn/hanzi-dict/search?param=%s' % char.encode('utf-8')
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Cookie': 'PHPSESSID=n9q5pkpuimhs1tdj6r80iq0702; _csrf=7b5176da068298669b0b5c2cd865b8ba12e2835b5615cde7c0f651e9bdb4b3b5a:2:{i:0;s:5:"_csrf";i:1;s:32:"9d5cgzBU1vND1p6QJ5HRTaxNYE0KzSPv";}',
                   }
        r = self.session.get(url)
        soup = BeautifulSoup(r.text)
        lq_variant = soup.find(id='lq-variant')
        return lq_variant

fetcher = VariantsFetcher()

if __name__ == '__main__':
    lq_variant = fetcher.fetch_variants(u'麤')
    print lq_variant