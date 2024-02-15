#Import statements
import time
import GoogleSheetAPI
import WebScraper
from datetime import datetime

#comment and clean up code
def storeResultsPerDay(api):

    revenu = api.read_cryptos_from_sheet("Junk's Results","B2")
    rows = api.read_cryptos_from_sheet("Results / Day Graph","B2:B")

    api.write_revenu_to_sheets("Results / Day Graph",revenu[0],len(rows)+2)
    api.write_revenu_to_sheets("Results / Day Graph",datetime.today(),len(rows)+2,"A")

def performCoreOperation(api,string):

    #read from spreadsheet
    cryptos = api.read_cryptos_from_sheet(string)

    print("Reading cryptos complete!")
    print("Starting to scrap prices .....")

    scraper = WebScraper.WebScraper()

    #Retrieves prices from CoinMarketCap
    prices = scraper.get_crytpos_prices(cryptos)

    print("Prices scraped!")
    print("Writing back to the google sheets....")

    # Writes back to GoogleSheets spreadsheet
    api.write_prices_to_sheets(len(prices)+2,prices,string)

    print("Google sheets updated!")

#dayPassed is sent to main to indicate if one day has passed
def main(dayPassed='N'):

    print('Starting to read from sheets')
    api = GoogleSheetAPI.GoogleSheetAPI()
    creds = api.authenticate_connection()
    api.buildTable(creds)

    print("Performing opeartion for Junk's Portfolio")
    performCoreOperation(api, "JunkPortfolio")

    print("Performing opeartion for Family's Portfolio")
    performCoreOperation(api, "FamilyPortfolio")

    if(dayPassed == 'Y'):
        storeResultsPerDay(api)


# Increases the time to wait between each scrap of CoinMarketCap by 3600s or 1 hour
# if wait time is 86400 seconds or 1 day then set the day passed parameter to Y
if __name__ == '__main__' :
    count = 0
    while True:
        time_wait = 3600
        count += time_wait

        if(count == 86400):
            main('Y')
            count = 0
        else:
            main()

        print(f'Waiting for 1 hour......')
        time.sleep(time_wait)