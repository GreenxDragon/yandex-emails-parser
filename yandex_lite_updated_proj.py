from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv


class YandexLiteBot:
    def __init__(self, login, password, opt):
        self.main_url = None
        self.login = login
        self.password = password
        self.opt = opt
        self.options = webdriver.ChromeOptions()
        self.set_options()
        self.path = os.path.split(__file__)[0] + os.path.sep
        self.driver = webdriver.Chrome(executable_path=f'{self.path}chromedriver', options=self.options)
        self.emails = []
        self.count_page = 1
        self.count_thread = 1

    def set_options(self):
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument("--disable-notifications")

    def authentication(self, url):
        """
        Logining in account
        :param url: str
        :return:
        """
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(5)
            # clicking on button "email or phone"
            login_button = self.driver.find_elements(by=By.CLASS_NAME,
                                                     value='AuthLoginInputToggle-type')
            if '@' in self.login:
                # mail
                login_button[0].click()
            else:
                # phone
                login_button[1].click()
            self.driver.implicitly_wait(4)
            # Input login
            self.driver.implicitly_wait(2)
            login = self.driver.find_element(by=By.ID, value='passp-field-login')
            login.clear()
            login.send_keys(self.login)
            # Press join button after that u have to input password
            sign_in = self.driver.find_element(by=By.ID, value='passp:sign-in')
            sign_in.click()
            self.driver.implicitly_wait(5)
            time.sleep(7)
            # Input password
            password = self.driver.find_element(by=By.ID, value='passp-field-passwd')
            password.clear()
            password.send_keys(self.password)
            # Sign in on email
            sign_in = self.driver.find_element(by=By.ID, value='passp:sign-in')
            sign_in.click()
            self.driver.implicitly_wait(50)
            time.sleep(45)
            self.main_url = url
        except Exception as ex:
            print(ex.__cause__)

    def getting_mails(self):
        """
        Getting mails from page
        :return: list_of_mails
        """
        try:
            ls = self.driver.find_element(
                By.ID, 'main').find_element(
                By.CLASS_NAME, 'b-messages').find_elements(
                By.CLASS_NAME, 'b-messages__message')
            return ls
        except:
            print(ex.__cause__)
            return None

    def reading_mail(self):
        emails = self.driver.find_elements(By.CLASS_NAME, 'b-message-head__email')
        for email in emails:
            txt_email = email.text
            if txt_email not in self.emails:
                self.emails.append(txt_email)
                print(txt_email)

    def its_thread(self):
        thread_url = self.driver.current_url

        def reading(urls):
            for mail_href in hrefs:
                print(mail_href)
                bot.driver.get(mail_href)
                bot.driver.implicitly_wait(4)
                bot.reading_mail()

        while True:
            mails_of_thread = self.getting_mails()
            if len(mails_of_thread) == 0:
                break
            hrefs = [mail.find_element(By.TAG_NAME, 'a').get_attribute('href') for mail in mails_of_thread]
            print(len(hrefs))
            reading(hrefs)
            self.count_thread += 1
            bot.driver.get(f'{thread_url}/page_number={self.count_thread}')
            self.driver.implicitly_wait(2)

    def csv_writer(self):
        name = ''
        if self.opt == 1:
            name = 'Inbox_'
        elif self.opt == 2:
            name = 'Sent_'
        elif self.opt not in (1, 2, 3):
            name = 'error'
            raise ValueError
        with open(f'{self.path}{name}{self.login[:5]}_emails.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Emails:'])
            for every in self.emails:
                writer.writerow([every.strip()])


def main():
    try:
        while True:
            ls_of_mails = bot.getting_mails()
            if len(ls_of_mails) == 0 or ls_of_mails is None:
                break
            href_and_class = {message.find_element(By.TAG_NAME, 'a').get_attribute('href'):
                              message.get_attribute('class') for message in ls_of_mails}
            for href in href_and_class:
                bot.driver.get(href)
                bot.driver.implicitly_wait(4)
                if 'thread' in href_and_class[href]:
                    bot.its_thread()
                else:
                    bot.reading_mail()
            bot.count_page += 1
            bot.driver.get(f'{bot.main_url}/page_number={bot.count_page}')
            bot.driver.implicitly_wait(4)
            time.sleep(2)
    except Exception as ex:
        print(ex.__cause__)


if __name__ == '__main__':
    bot = YandexLiteBot(input("Enter email or phone number: "), input("Enter paaasword: "),
                        int(input('From where go gather emails:\n Enter:\n 1 if <inbox>,\n'
                                  ' 2 - if <sent>\n')))
    try:
        if bot.opt == 2:
            bot.authentication('https://mail.yandex.ru/lite/sent')
            main()
        if bot.opt == 1:
            bot.authentication('https://mail.yandex.ru/lite/inbox')
            main()
        else:
            raise ValueError
    except Exception as ex:
        print(ex.__cause__)
    finally:
        bot.csv_writer()
        bot.driver.close()
        bot.driver.quit()
