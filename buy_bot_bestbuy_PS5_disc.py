from selenium import webdriver
from config import info_keys
import time
from requests_html import HTMLSession, AsyncHTMLSession
from bs4 import BeautifulSoup
from twilio.rest import Client
from datetime import datetime

def timeme(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))
        print("Execution time: {}".format((endTime - startTime) / 1000))
        return result

    return wrapper


@timeme  # this will run the timeme function when function below is executed
def order(k, bestbuy_url):
    browser.get(bestbuy_url)

    browser.find_element_by_xpath('//*[@id="test"]/button/span/div/span').click()  # Add to cart
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="cartIcon"]/div[2]/div/div/div/section/div/button/span').click()  # View Cart

    time.sleep(7)
    element_checkout = browser.find_element_by_xpath(
        '//*[@id="root"]/div/div/div[4]/div[2]/div[2]/section/div/section/section[2]/div[2]/div/a/span/span')
    browser.execute_script("arguments[0].click();", element_checkout)

    browser.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div/div[2]/div/div[2]/a/span').click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="email"]').send_keys(k['emailreal'])
    browser.find_element_by_xpath('//*[@id="firstName"]').send_keys(k['first'])
    browser.find_element_by_xpath('//*[@id="lastName"]').send_keys(k['last'])
    browser.find_element_by_xpath('//*[@id="addressLine"]').send_keys(k['fulladdress'])
    browser.find_element_by_xpath('//*[@id="city"]').send_keys(k['city'])
    browser.find_element_by_xpath('//*[@id="postalCode"]').clear()
    browser.find_element_by_xpath('//*[@id="postalCode"]').send_keys(k['postalcode'])
    browser.find_element_by_xpath('//*[@id="phone"]').send_keys(k['tel'])
    browser.find_element_by_xpath('//*[@id="posElement"]/section/section[1]/button/span').click()
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="shownCardNumber"]').send_keys(k['kard_number'])
    browser.find_element_by_xpath('//*[@id="expirationMonth"]/option[5]').click()
    browser.find_element_by_xpath('//*[@id="expirationYear"]/option[2]').click()
    browser.find_element_by_xpath('//*[@id="cvv"]').send_keys(k['kard_v'])
    browser.find_element_by_xpath('//*[@id="posElement"]/section/section[1]/button/span').click()


    # =======================PLACE ORDER CLICK BUTTON==============================
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="posElement"]/section/section[1]/button/span').click()  #  Place order


def message_tuco(sms):
    # Account SID from twilio.com/console
    account_sid = "notforsharing"
    # Auth Token from twilio.com/console
    auth_token = "notforsharing"

    client = Client(account_sid, auth_token)
    message = client.messages.create(
                                    to="+14034448888",
                                    from_="+15873176186",
                                    body=sms
                                    )


def get_bestbuy_status(bestbuy_url):
    """
    To Check Stock Status of The Source
    """
    while 1:
        session = HTMLSession()
        r = session.get(bestbuy_url)

        soup = BeautifulSoup(r.content, 'html.parser')
        try:
            a = soup.find('span', class_="availabilityMessage_1MO75 container_3LC03").text
            if a == 'Coming soon':
                print("Just checked ", bestbuy_url, ' ', datetime.now())
        except:
            try:
                a = soup.find('div', class_='header').text
                if a == 'Page not found.':
                    print("Just checked ", bestbuy_url, ' ', datetime.now())
            except:
                message_tuco("IN STOCK: " + bestbuy_url)
                break

        time.sleep(20)


if __name__ == '__main__':

    url = 'https://www.bestbuy.ca/en-ca/product/playstation-5-console-online-only/14962185'
    bestbuy_url = get_bestbuy_status(url)

    # the browser driver needs to be outside of the function, otherwise the browser will close at the end
    browser = webdriver.Chrome("bin\\chromedriver.exe")

    # keys attribute from config.py file used when function called
    order(info_keys, bestbuy_url)

    browser.close()
    browser.quit()