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
    acls = None

    def __init__(self, username, password):
        self.macs = {}
        self.driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
        self.driver.implicitly_wait(30)
        self.driver.set_window_size(1024, 768)

        self.driver.get(self.__class__.logon_url)
        self.driver.find_element_by_css_selector('[name="username"]').send_keys(username)
        self.driver.find_element_by_css_selector('[name="password"]').send_keys(password)
        self.driver.find_element_by_css_selector('[name="ok"]').click()
        time.sleep(3)  # wait for the authentication page to be loaded.
        self.get_acls()

    def add_mac(self, mac, acl_list=None):
        if acl_list is None:
            acl_list = self.__class__.acls[-1]
        else:
            acl_list = acl_list

        if not self.exist_mac(mac):
            self.driver.get(self.__class__.conf_acl_url)  # go to configuration page.
            self.driver.find_element_by_css_selector(f'[id="{acl_list}"]').click()
            self.driver.find_element_by_css_selector(f'[id="mac"]').send_keys(mac)
            self.driver.find_element_by_css_selector('[id="create-new-station"]').click()
            self.driver.find_element_by_css_selector('[id="ok-acl"]').click()
            time.sleep(2)  # wait for data syncing.
            return 'success'
        else:
            return 'failed, MAC existed'

    def remove_mac(self, mac, acl_list=None):
        if acl_list is None:
            acl_list = self.__class__.acls[-1]
        else:
            acl_list = acl_list

        x = self.exist_mac(mac)
        if x:
            self.driver.get(self.__class__.conf_acl_url)  # go to configuration page.
            self.driver.find_element_by_css_selector(f'[id="{acl_list}"]').click()
            #  TODO: remove the specified mac.
            return 'success'
        else:
            return 'failed, MAC doesn\'t exist'

    def all_mac(self):
        self.driver.get(self.__class__.conf_acl_url)  # go to configuration page.
        for acl in self.__class__.acls:  # loop through acl list.
            self.driver.find_element_by_css_selector(f'[id="{acl}"]').click()  # click "EDIT" button.
            macs = self.driver.find_element_by_css_selector('#staTable').text  # get MACs.
            filtered_macs = tuple(macs.replace(' delete', '').replace('\n', ' ').lower().split(' '))  # filter out unwanted charactors.
            self.macs.setdefault(acl, filtered_macs)  # put MACs into dictionary with acl as key.
        return self.macs

    def exist_mac(self, mac):
        for k, v in self.all_mac().items():  # loop through MAC list.
            if mac in v:  # if target mac in the MAC list.
                return k  # return acl.
        return False

    def get_acls(self):
        self.driver.get(self.__class__.conf_acl_url)  # go to configuration page.
        acl_objs = self.driver.find_element_by_css_selector('table#acl.listTable > tbody').find_elements_by_css_selector('td.action > span')  # get acl lists.
        self.__class__.acls = tuple([i.get_attribute('id') for i in acl_objs if 'edit' in i.get_attribute('id')])  # filter out unwanted charactors.
        return self.__class__.acls

    def __repr__(self):
        pass
        #  TODO: return something.

    def __del__(self):
        return self.driver.quit()


if __name__ == '__main__':
    user = os.environ.get('RUCKUS_USER')
    pw = os.environ.get('RUCKUS_PASS')
    mac = 'cc:cc:cc:cc:cc:cc'

    r1 = Ruckus(user, pw)
    print(r1.all_mac())

    del r1

