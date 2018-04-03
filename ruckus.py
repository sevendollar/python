#!/usr/bin/python

import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re

# profile = webdriver.FirefoxProfile()
# profile.default_preferences['webdriver_assume_untrusted_issuer'] = False
# profile.update_preferences()
# profile.accept_untrusted_certs = True
# driver = webdriver.Firefox(firefox_profile=profile, executable_path='.\geckodriver.exe')

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# driver = webdriver.Chrome(chrome_options=options)


class Ruckus:
    logon_url = 'https://wifi.cvl.com.tw/admin/login.jsp'
    dashboard_url = 'https://wifi.cvl.com.tw/admin/dashboard.jsp'
    conf_acl_url = 'https://wifi.cvl.com.tw/admin/conf_acls.jsp'
    acl = 'edit-acl-2'
    acls = None

    def __init__(self, username, password):
        self.driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
        self.driver.implicitly_wait(30)
        self.driver.set_window_size(1024, 768)

        self.driver.get(self.__class__.logon_url)
        self.driver.find_element_by_css_selector('[name="username"]').send_keys(username)
        self.driver.find_element_by_css_selector('[name="password"]').send_keys(password)
        self.driver.find_element_by_css_selector('[name="ok"]').click()
        time.sleep(3)  # wait for the authentication page to be loaded.
        self.get_acls()


    def add_mac(self, mac):
        if not self.exist_mac(mac):
            self.driver.get(self.__class__.conf_acl_url)
            self.driver.find_element_by_css_selector(f'[id="{self.__class__.acl}"]').click()
            self.driver.find_element_by_css_selector(f'[id="mac"]').send_keys(mac)
            self.driver.find_element_by_css_selector('[id="create-new-station"]').click()
            self.driver.find_element_by_css_selector('[id="ok-acl"]').click()
            return 'success added the mac.'
        else:
            return 'mac existed.'

    def remove_mac(self, mac):
        # todo remove the specified mac.
        if self.exist_mac(mac):
            pass
            return 'success remove the mac.'
        else:
            return "mac doesn't exist."

    def all_mac(self):
        self.driver.get(self.__class__.conf_acl_url)
        self.driver.find_element_by_css_selector(f'[id="{self.__class__.acl}"]').click()
        # self.driver.find_element_by_css_selector(f'[id="edit-acl-1"]').click()
        macs = self.driver.find_element_by_css_selector('#staTable').text
        return tuple(macs.replace(' delete', '').replace('\n', ' ').lower().split(' '))

    def exist_mac(self, mac):
        if mac in self.all_mac():
            return True
        return False

    def get_acls(self):
        self.driver.get('https://wifi.cvl.com.tw/admin/conf_acls.jsp')
        acl_objs = self.driver.find_element_by_css_selector('table#acl.listTable > tbody').find_elements_by_css_selector('td.action > span')  # get acl lists
        self.__class__.acls = tuple([i.get_attribute('id') for i in acl_objs if 'edit' in i.get_attribute('id')])  # filter out the acl
        return self.__class__.acls

    def __del__(self):
        return self.driver.quit()


if __name__ == '__main__':
    user = os.environ.get('RUCKUS_USER')
    pw = os.environ.get('RUCKUS_PASS')

    r1 = Ruckus(user, pw)
    x = r1.get_acls()
    print(x)

    del r1

