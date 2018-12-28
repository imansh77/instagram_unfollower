from conf import Settings

import logging
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import action_chains


class Init:
	"""must have class in all modules using selenium and log"""
	def __init__(self):
		logging.basicConfig(
			filename='not_follower.log', level=logging.INFO, format='%(levelname)s: [%(asctime)s] %(message)s')
		self.logger = logging.getLogger(__name__)
		logging.getLogger().addHandler(logging.StreamHandler())
		chromeOptions = webdriver.ChromeOptions()
		prefs = {'profile.managed_default_content_settings.images': 2, 'disk-cache-size': 4096}
		chromeOptions.add_experimental_option("prefs", prefs)
		self.driver = webdriver.Chrome(chrome_options=chromeOptions)


class OpeningLinks(Init):

	def open_login_page(self):
		try:
			self.driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
			element = WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.CLASS_NAME, 'DINPA')))
			self.logger.info("login page is successfully opened")
		except:
			self.logger.error("something went wrong, check your internet connection!")
			sys.exit(0)


class Credentials(OpeningLinks):

	def login(self):
		self.open_login_page()
		try:
			username = Settings.login_username
			password = Settings.login_password
			self.driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
			self.driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
			self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/button').click()
			if "Sorry" in self.driver.page_source:
				self.logger.error("The Entered password is wrong.")
				sys.exit(0)
		except:
			pass

	def check_if_logged(self):
		self.login()
		try:
			WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'm0NAq')))
		except:
			return False

	def second_auth(self):
		if self.check_if_logged() is False:
			n = input('enter: ')
			self.driver.find_element_by_xpath('//*[@class="_2hvTZ pexuQ zyHYP"]').send_keys(n)
			self.driver.find_element_by_xpath(
				'//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]').click()


Credentials().second_auth()
