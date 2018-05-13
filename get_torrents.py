import os
import time
from getpass import getpass
from string import Template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Crawler:
    def __init__(self, url, browser=None):
        self.url = url
        self.browser = browser
        while True:
            # use the pre-defined value or let the user to input it from the console.
            user_defined_browser = (
               self.browser
               or
               input('preferred browser?(default:chrome)\n(press enter to go for the default...) ')
            )

            # go for chrome browser which is the default.
            if user_defined_browser in ('chrome', ''):
                self.options = webdriver.ChromeOptions()
                self.options.add_argument('--headless')
                self.options.add_argument('--allow-running-insecure-content')
                self.options.add_argument('--allow-insecure-localhost')
                self.options.add_argument('--ignore-certificate-errors')
                # self.options.add_argument('--no-sandbox')
                # self.options.add_argument('--window-size=800,600')
                self.options.add_argument('--reduce-security-for-testing')
                # self.options.add_argument('--sync-allow-insecure-xmpp-connection')

                capabilities = webdriver.DesiredCapabilities.CHROME.copy()
                capabilities['acceptSslCerts'] = True
                capabilities['acceptInsecureCerts'] = True

                self.driver = webdriver.Chrome(
                    chrome_options=self.options,
                    executable_path=os.path.join(os.path.abspath('.'), 'chromedriver'),
                    desired_capabilities=capabilities,
                )
                break
            # or go for firefox browser.
            elif user_defined_browser == 'firefox':
                self.options = webdriver.FirefoxOptions()
                self.options.add_argument('--no-sandbox')
                self.options.add_argument('--window-size=1420,1080')
                # self.options.add_argument('--headless')
                self.options.add_argument('--disable-gpu')
                self.options.add_argument('--ignore-certificate-errors')
                self.driver = webdriver.Firefox(
                    executable_path=os.path.join(os.path.abspath('.'), 'geckodriver'),
                    firefox_options=self.options,
                )
                break
            else:
                print("choose either 'firefox' or 'chrome'...\n")

    def __enter__(self):
        print('<<< starting browser... >>>')
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
        print('<<< closing browser... >>>')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.url})'


url = 'https://wifi.cvl.com.tw/admin/login.jsp'
RUCKUS_USER = (
    os.environ.get('RUCKUS_PASS')
    or
    Template(f'$ruckus_user').substitute(ruckus_user=input('Ruckus User: '))
)
RUCKUS_PASS = (
        os.environ.get('RUCKUS_PASS')
        or
        Template(f'$ruckus_pass').substitute(ruckus_pass=getpass('Ruckus Password: '))
)
ff = Crawler(url, 'chrome')

with ff as driver:
    driver.get(url)
    print(f'first title: {driver.title}')
    driver.get_screenshot_as_file(os.path.join(os.path.abspath('.'), 'chrome.png'))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(RUCKUS_USER)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(RUCKUS_PASS)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "ok"))).click()

    # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'company')))
    # num_of_clients = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'num-client')))
    num_of_clients = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'num-client')))
    uptime = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'sysuptime')))
    print(uptime.text)
    print(num_of_clients.text)

    print(f'last title: {driver.title}')
    driver.get_screenshot_as_file(os.path.join(os.path.abspath('.'), 'chrome2.png'))
