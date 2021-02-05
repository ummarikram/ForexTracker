import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib

URL = 'https://www.dailyfx.com/forex-rates' # The website 

headers = {"User Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.191'}

GmailUsername = 'username@gmail.com'
GmailPassword = 'password'

TargetCurrency = 'EUR/USD' # Add as per your requirement
TargetRate = '0.0000' # Add upto 4 decimal place

def getRates():

    CurrencyNames = []   
    CurrencyRates = []
    Values = []

    page = requests.get(URL, headers = headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    Currencies = soup.find_all(class_ = "dfx-instrumentTiles__singleTile col-12 col-md-6 col-lg-4")
    
    # Get Currency Names
    for Currency in Currencies:
        CurrencyNames.append(str(Currency.find(class_ = 'dfx-font-size-3 font-weight-bold mr-1').get_text()).strip())

    allId = soup.find_all("svg",attrs={"data-value" : True})

    # Get Floating Rates
    for item in allId:
        Values.append(item['data-value'])

    # Store Rates as Strings
    for value in Values:
        CurrencyRates.append((str(value).split(',')[-1]))

    # Create Object from pd module
    ForexRates = pd.DataFrame({'Currency': CurrencyNames, 'Rate' : CurrencyRates})

    # Create CSV
    ForexRates.to_csv('Forex.csv')
    
    print('CSV CREATED!')
    
    if (TargetRate != '0.0000'):
        # For Email Sending
        for index in range(len(CurrencyNames)):
            if (CurrencyNames[index] == TargetCurrency):  # if the targeted currency and rate exists then send mail
                if (CurrencyRates[index] >= TargetRate):
                    sendEmail()
                break
            
def sendEmail():
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(GmailUsername, GmailPassword)

    subject = TargetCurrency + ' RATE ALERT!'

    body = TargetCurrency + ' has reached your targeted rate of ' + TargetRate

    msg = f"Subject: {subject}\n\n\n\n{body}"

    server.sendmail(
        GmailUsername, # From
        GmailUsername, # To
        msg            # Message
    )

    print('EMAIL SENT!')

    server.quit()

getRates()