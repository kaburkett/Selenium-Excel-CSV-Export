# -*- coding: utf-8 -*-
# Script by: Kyle Burkett
# Date: 09/13/2016
# Python Version: 2.7
# Purpose: export browser items to csv file
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
#import for csv file writing :)
import csv
import sys
import time
import datetime
from os import fsync

class Exportcontacts(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://manage.firepoint.net/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_exportcontacts(self):
		#
		#SET ALL TEST VARIABLES THIS SECTION
		#
		leads = 10 #Set Number of Leads as integer to cycle through
		lsid = 10 #set unique lsid parameter as integer found in management lead panel url
		username = 'example@example.com' #set username as string
		password = 'yourpassword' #set password as string
		filename = 'example.csv' #do include filetype, declare as string
		#
		#Begin script
		#
		lsidstr = str(lsid)
		count = str(leads)
		driver = self.driver
		driver.get(self.base_url + "/dashboard")
		driver.find_element_by_id("username").clear()
		driver.find_element_by_id("username").send_keys(username)
		driver.find_element_by_id("password").clear()
		driver.find_element_by_id("password").send_keys(password)
		driver.find_element_by_xpath("//button[@type='submit']").click()
		driver.get("https://manage.firepoint.net/leads/564575/details?count="+ count +"&idx=0&lsid=" + lsidstr)
		with open(filename, 'w') as fp:
			a = csv.writer(fp, delimiter=',')
			data = [['Full Name', 'Phone Number', 'E-mail']]
			a.writerows(data)
			for x in range (0,leads):
				y = str(x)
				driver.get(self.base_url + "leads/573808/next?count="+ count +"&idx=" + y + "&lsid=" + lsidstr)
				try:
					name = driver.find_element_by_css_selector("h1.contact-name").text
				except:
					name = 'Not Found'
				try:
					number = driver.find_element_by_css_selector("button#dLabel > span.item-text").text
				except:
					number = 'Not Found'
				try:
					email = driver.find_element_by_css_selector("a.lead-email > span.icon-text").text
				except:
					email = 'Not Found'
				data = [[name, number, email]]
				a.writerows(data)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
