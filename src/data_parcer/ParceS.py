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
        news_head = soup.find_all('div', class_='text_blk')
        all_text = [t.text.strip().split('\n')[0] for t in news_head]
        tranliterate_text = list(map(lambda x: translit(x.lower(), 'ru', reversed=True).replace(' ', '-'), all_text))
        return tranliterate_text



Fork_p = ForklogPars('https://forklog.com/news')