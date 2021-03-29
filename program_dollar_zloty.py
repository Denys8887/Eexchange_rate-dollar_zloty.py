import requests  # URL processing module
from bs4 import BeautifulSoup  # HTML module
import time  # Module for stopping the program
import smtplib  # Module for working with mail


# Main class
class Currency:
    # Link to the desired page
    dollar_zloty = 'https://www.google.com/search?sxsrf=ALeKk00zR1CEOE9NBFQeTqesuNDLo0MB0A%3A1616074016153&ei' \
                   '=IFVTYObQCPiFwPAP5p-goAI&q=dollar++zloty&oq=dollar++zloty&gs_lcp' \
                   '=Cgdnd3Mtd2l6EAMyCggAEMsBEEYQggIyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBgg' \
                   '=AEBYQHjIGCAAQFhAeMgYIABAWEB46BwgAEEcQsAM6BAgAEA06BggAEA0QHjoMCAAQChDLARBGEIICOggIABAWEAoQHjoCCAA' \
                   '=6BggAEAoQAzoECAAQClD5CVjGE2DlFWgBcAJ4AIABYogBuAOSAQE1mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=' \
                   '=gws-wiz&ved=0ahUKEwjm4Kbt-LnvAhX4AhAIHeYPCCQQ4dUDCA0&uact=5 '
    # Headers to be passed along with the URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36'}

    current_converted_price = 0
    difference = 0.3  # The difference after which the message will be sent to the mail

    def __init__(self):
        # Setting the currency rate when creating an object
        self.current_converted_price = float(self.get_currency_price().replace(",", "."))

    # Method for obtaining the currency rate
    def get_currency_price(self):
        # Parse the entire page
        full_page = requests.get(self.dollar_zloty, headers=self.headers)

        # We work with BeautifulSoup
        soup = BeautifulSoup(full_page.content, 'html.parser')

        # We get the value what we need and return it
        convert = soup.findAll("span", {"class": "DFlfde", "data-precision": 2})
        return convert[0].text

    # Checking currency change
    def check_currency(self):
        currency = float(self.get_currency_price().replace(",", "."))
        if currency >= self.current_converted_price + self.difference:
            print("The course has grown a lot, maybe it's time to do something?")
            self.send_mail()
        elif currency <= self.current_converted_price - self.difference:
            print("The course has dropped a lot, maybe it's time to do something?")
            self.send_mail()

        print(f"Rate now is: 1$ = {str(currency)}zl")
        time.sleep(3)  # Sleep program for 3 seconds
        self.check_currency()

    # Sending mail via SMTP
    def send_mail(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('YOUR MAIL', 'PASSWORD')

        subject = 'Currency mail'
        body = 'Currency has been changed!'
        message = f'Subject: {subject}\n{body}'

        server.sendmail(
            'Who sends',
            'recipient',
            message
        )
        server.quit()


# Object creation and method invocation
currency = Currency()
currency.check_currency()
