import requests
from bs4 import BeautifulSoup

class WebScraper():

    #Scarps price information from CoinMarketCap based on the list of cryptos passed
    def get_crytpos_prices(self,cryptoList):

        prices = []

        for crypto in cryptoList:

            #Goes to the specfic url of each coin to scrap
            url = f"https://coinmarketcap.com/currencies/{crypto[0]}"

            response = requests.get(url)
            soup = BeautifulSoup(response.content,'html.parser')

            #Searaching for a span with class  sc-f70bb44c-0 jxpCgO base-text or sc-f70bb44c-0 eZIItc base-text. These
            #classes include the price information required.
            price = soup.find("span",class_ = "sc-f70bb44c-0 jxpCgO base-text")

            if(price == None):
                price = soup.find("span",class_="sc-f70bb44c-0 eZIItc base-text")

            prices.append(price.text)

        return prices