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

    def parse_s(self, payload: str, headers: str):  # change (payload, headers) on class variables or object variables
        """Target resource parsing method.

        Args:
            payload (str): Payloads.
            headers (str): Headers.

        Returns:
            None
        """
        response = requests.request("GET", self.base_url, data=payload, headers=headers)
        text = response.text
        soup = bs4.BeautifulSoup(text, features='html.parser')
        return soup


class ForklogPars(BaseParser):
    def parse_s(self, payload: str, headers: str) -> list[str]:  # change (payload, headers) on class variables or object variables
        """Target resource parsing method.

        Args:
            payload (str): Payloads.
            headers (str): Headers.

        Returns:
            all_href_parse (list[str]): link to each article
        """
        response = requests.request("GET", self.base_url, data=payload, headers=headers)
        text = response.text
        soup = bs4.BeautifulSoup(text, features='html.parser')
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
            data_url (str): url for artickle concatnate

        Returns:
            None
        """
        super().__init__(base_url)
        self.data_url = data_url

    def parse_s(self, payload: str, headers: str) -> list[str]:  # change (payload, headers) on class variables or object variables
        """Target resource parsing method.

        Args:
            payload (str): Payloads.
            headers (str): Headers.

        Returns:
            all_href_parse (list[str]): link to each article
        """
        response = requests.request("GET", self.base_url, data=payload, headers=headers)
        text = response.text
        soup = bs4.BeautifulSoup(text, features='html.parser')
        articles_2 = soup.find_all('a', class_="headline__HeadlineLink-sc-1uoawmp-0 jbDMkW")
        all_href_parse = [self.data_url + t['href'] for t in articles_2]
        return all_href_parse



Fork_p = ForklogPars('https://forklog.com/news')
CoDe_p = CoDePars('https://www.coindesk.com/livewire/', 'https://www.coindesk.com')