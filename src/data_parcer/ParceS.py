import requests
import bs4
from transliterate import translit


class BaseParser:
    def __init__(self, base_url: str) -> None:
        """Initialize BaseParser object.

        Args:
            base_url (str): base domain for parsing.

        Returns:
            None
        """
        self.base_url = base_url

    def parse_href(self, payload: str, headers: str, url: str):  # change (payload, headers) on class variables or object variables
        """Target resource parsing method.

        Args:
            payload (str): Payloads.
            headers (str): Headers.
            url (str): URL to parce.

        Returns:
            None ### change no None
        """
        response = requests.request("GET", url, data=payload, headers=headers)
        text = response.text
        soup = bs4.BeautifulSoup(text, features='html.parser')
        return soup


class ForklogPars(BaseParser):
    def custom_parse_href(self, payload: str, headers: str) -> list[str]:  # change (payload, headers) on class variables or object variables
        """Target resource parsing method.

        Args:
            payload (str): Payloads.
            headers (str): Headers.

        Returns:
            all_href_parse (list[str]): link to each article
        """
        soup = self.parse_href(url=self.base_url, payload=payload, headers=headers)
        news_head = soup.find_all('div', class_='text_blk')
        all_text = [t.text.strip().split('\n')[0] for t in news_head]
        trans_table = {ord(':'): None, ord('«'): None, ord('»'): None, ord(' '): '-'}
        tranliterate_text = list(map(lambda x: translit(x.lower(), 'ru', reversed=True).translate(trans_table), all_text))
        all_href_parse = list(map(lambda x: self.base_url + '/' + x.replace('ija', 'iya'), tranliterate_text)) # write parsing tests for these links
        return all_href_parse

class CoDePars(BaseParser):
    def __init__(self, base_url: str, data_url: str) -> None:
        """Initialize CoDePars object.

        Args:
            base_url (str): base domain for parsing.
            data_url (str): Url for artickle concatnate.

        Returns:
            None
        """
        super().__init__(base_url)
        self.data_url = data_url

    def custom_parse_href(self, payload: str, headers: str) -> list[str]:  # change (payload, headers) on class variables or object variables
        """Target resource parsing method.

        Args:
            payload (str): Payloads.
            headers (str): Headers.

        Returns:
            all_href_parse (list[str]): link to each article
        """
        soup = self.parse_href(url=self.base_url, payload=payload, headers=headers)
        articles_2 = soup.find_all('a', class_="headline__HeadlineLink-sc-1uoawmp-0 jbDMkW")
        all_href_parse = [self.data_url + t['href'] for t in articles_2]
        return all_href_parse

    def parce_artickle(self, href_list: list[str], payload: str, headers: str) -> list[str]:
        """parsing articles on the site.

        Args:
            href_list (str): All links for parsing.
            payload (str): Payloads.
            headers (str): Headers.

        Returns:
            all_text (list[str]): text of all articles

        """
        res = []
        for href in href_list:
            soup = self.parse_href(url=href, payload=payload, headers=headers)
            article = soup.find_all('div', class_="common-textstyles__StyledWrapper-sc-18pd49k-0 eSbCkN")
            article = [i.text for i in article if not i.find(lambda tag: tag.name == 'a' and tag.get('target') == '_blank')]
            res.append(' '.join(article))
        return res

class CryptoNewsParse(BaseParser):
    def custom_parse_href(self, payload: str, headers: str) -> list[str]:  # change (payload, headers) on class variables or object variables
        """Target resource parsing method.

        Args:
            payload (str): Payloads.
            headers (str): Headers.

        Returns:
            all_data (list[str]): link to each article
        """
        soup = self.parse_href(url=self.base_url, payload=payload, headers=headers)
        articles_2 = soup.find_all('a', class_="title", string=True)
        all_data = [self.base_url+t['href'] for t in articles_2]
        return all_data

    def parce_artickle(self, href_list: list[str], payload: str, headers: str) -> list[str]:
        """parsing articles on the site.

        Args:
            href_list (str): All links for parsing.
            payload (str): Payloads.
            headers (str): Headers.

        Returns:
            all_text (list[str]): text of all articles

        """
        res = []
        for href in href_list:
            soup = self.parse_href(url=href, payload=payload, headers=headers)
            article = soup.find_all('div', class_="cn-content")
            res.append(article[0].text)
            try:
                res.append(article[0].text)
            except IndexError:
                continue
        return res

Fork_p = ForklogPars('https://forklog.com/news')
CoDe_p = CoDePars('https://www.coindesk.com/livewire/', 'https://www.coindesk.com')
Cr_news = CryptoNewsParse('https://cryptonews.net')