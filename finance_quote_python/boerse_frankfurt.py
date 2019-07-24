'''
Price downloader for Boerse Frankfurt (FWB)

The new boerse-frankfurt.de
https://www.boerse-frankfurt.de/etp/IE00B810Q511

https://api.boerse-frankfurt.de/data/quote_box?isin=IE00BKX55Q28&mic=XFRA
'''
import logging
from pricedb import SecuritySymbol, PriceModel


class FwbDownloader:
    ''' FWB '''
    def __init__(self):
        self.namespace = "FWB"
        self.logger = logging.getLogger(__name__)

    def download(self, symbol: SecuritySymbol, currency: str) -> PriceModel:
        ''' download the price '''
        import urllib.parse
        import urllib.request

        if not symbol.namespace:
            raise ValueError(f"Namespace not sent for {symbol}")

        self.logger.debug(f"fetching price from FWB.")

        url = self.get_security_url(symbol)

        # download
        with urllib.request.urlopen(url) as response:
            html = response.read()

        if not html:
            return None

        # parse
        price = self.parse_price(html)

        return None

    def get_security_url(self, security: SecuritySymbol) -> str:
        ''' Mapping the security to the price URL '''
        if security.namespace != self.namespace:
            raise ValueError("Wrong exchange requested!")

        sec_codes = {
            "VGOV": "IE00B42WWV65",
            "VMID": "IE00BKX55Q28",
            "VUKE": "IE00B810Q511"
        }
        isin = sec_codes[security.mnemonic]

        #url = f"https://www.boerse-frankfurt.de/etp/{isin}"
        url = f"https://api.boerse-frankfurt.de/data/quote_box?isin={isin}&mic=XFRA"

        return url

    def parse_price(self, html: str) -> PriceModel:
        ''' Get the price from HTML '''
        from bs4 import BeautifulSoup

        result = PriceModel()
        soup = BeautifulSoup(html, 'html.parser')

        price_el = soup.find(id='last-price-value')

        return ''
