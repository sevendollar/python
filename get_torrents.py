import os
import time
from getpass import getpass
from string import Template
import functools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def timer(origin_func):
    @functools.wraps(origin_func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        results = origin_func(*args, **kwargs)
        end_time = round(time.time() - start_time)
        print(f'total cost of time: {end_time} seconds.')
        return results
    return wrapper


class Crawler:
    def __init__(self, url, browser=None):
        self.url = url
        self.browser = browser
        while True:
            # use the pre-defined value or let the user to input it from the console.
            self.user_defined_browser = (
               self.browser or
               input('preferred browser?(default:phantomjs)\n(press enter to go for the default...) ')
            )
            # go for phantomjs browser which is the default.
            if self.user_defined_browser in ('phantomjs', ''):
                # set the chrome webdriver executable depends on the OS.
                self.executable = (lambda: 'phantomjs' if os.sys.platform == 'linux' else 'phantomjs.exe')()
                self.driver = webdriver.PhantomJS(
                    service_args=['--ignore-ssl-errors=true'],
                    executable_path=os.path.join(os.path.abspath('.'), self.executable),
                )
                self.driver.set_window_size(1024, 768)
                break
            # go for chrome browser
            elif self.user_defined_browser == 'chrome':
                # set the chrome webdriver executable depends on the OS.
                self.executable = (lambda: 'chromedriver' if os.sys.platform == 'linux' else 'chromedriver.exe')()
                self.options = webdriver.ChromeOptions()
                self.options.add_argument('--headless')
                self.options.add_argument('--allow-running-insecure-content')
                self.options.add_argument('--allow-insecure-localhost')
                self.options.add_argument('--ignore-certificate-errors')
                # self.options.add_argument('--no-sandbox')
                self.options.add_argument('--window-size=1024,768')
                self.options.add_argument('--reduce-security-for-testing')
                # self.options.add_argument('--sync-allow-insecure-xmpp-connection')

                self.capabilities = webdriver.DesiredCapabilities.CHROME.copy()
                self.capabilities['acceptSslCerts'] = True
                self.capabilities['acceptInsecureCerts'] = True

                self.driver = webdriver.Chrome(
                    chrome_options=self.options,
                    executable_path=os.path.join(os.path.abspath('.'), self.executable),
                    desired_capabilities=self.capabilities,
                )
                break
            # or go for firefox browser.
            elif self.user_defined_browser == 'firefox':
                # set the firefox webdriver executable depends on the OS.
                self.executable = (lambda: 'geckodriver' if os.sys.platform == 'linux' else 'geckodriver32.exe')()
                self.options = webdriver.FirefoxOptions()
                # self.options.add_argument('--no-sandbox')
                # self.options.add_argument('--window-size=1420,1080')
                # self.options.add_argument('--headless')
                # self.options.add_argument('--disable-gpu')
                self.options.add_argument('--ignore-certificate-errors')

                self.capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
                self.capabilities['acceptSslCerts'] = True
                self.capabilities['acceptInsecureCerts'] = True

                self.driver = webdriver.Firefox(
                    executable_path=os.path.join(os.path.abspath('.'), self.executable),
                    firefox_options=self.options,
                    desired_capabilities=self.capabilities,
                )
                break
            else:
                print("choose either 'firefox' or 'chrome'...\n")

    def __enter__(self):
        print('<<< starting browser... >>>')
        # if calling the Class with a url parameter, do the "get url " method.
        if self.url:
            self.driver.get(self.url)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
        print('<<< closing browser... >>>')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.url})'


@timer
def number_of_clients():
    ff = Crawler(url, 'chrome')
    with ff as driver:
        driver.get_screenshot_as_file(os.path.join(os.path.abspath('.'), 'chrome.png'))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(RUCKUS_USER)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(RUCKUS_PASS)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "ok"))).click()
        success_logon = WebDriverWait(driver, 20).until(EC.title_contains('Dashboard'))
        print((lambda x: '>>> Successfully Logon! <<<' if x else '>>> Failed Logon! <<<')(success_logon))

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'company')))
        num_of_clients = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'num-client'))).text
        # num_of_clients = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'num-client')))
        print(f'number of clients: {num_of_clients}')

        driver.get_screenshot_as_file(os.path.join(os.path.abspath('.'), 'chrome2.png'))


if __name__ == '__main__':
    url = 'https://wifi.cvl.com.tw/admin/login.jsp'
    RUCKUS_USER = (os.environ.get('RUCKUS_USER') or
                   Template(f'$ruckus_user').substitute(ruckus_user=input('Ruckus User: ')))
    RUCKUS_PASS = (os.environ.get('RUCKUS_PASS') or
                   Template(f'$ruckus_pass').substitute(ruckus_pass=getpass('Ruckus Password: ')))
    number_of_clients()