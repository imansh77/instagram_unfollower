from conf import Settings

import sys
import time
import pickle
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Init:
	"""must have class in all modules using selenium and log"""
	def __init__(self):
		logging.basicConfig(
			filename='not_follower.log', level=logging.INFO, format='%(levelname)s: [%(asctime)s] %(message)s')
		self.logger = logging.getLogger(__name__)
		logging.getLogger().addHandler(logging.StreamHandler())

		options = webdriver.ChromeOptions()
		prefs = {'profile.managed_default_content_settings.images': 2, 'disk-cache-size': 4096}
		options.add_experimental_option("prefs", prefs)
		options.add_argument("user-data-dir=/tmp/tarun")
		self.driver = webdriver.Chrome(chrome_options=options,executable_path='/Coding/GitHub/insta_unfollower/crawler/chromedriver')

class Cookie(Init):

	def saving_cookies(self):
		pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

	def loading_cookies(self):
		for cookie in pickle.load(open("cookies.pkl", "rb")):
			self.driver.add_cookie(cookie)


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


class Credentials(OpeningLinks, Cookie):

	def login(self):
		self.open_login_page()
		try:
			username = Settings.login_username
			password = Settings.login_password
			self.driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
			self.driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
			self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/button').click()
			time.sleep(1)
			if "Sorry, your password was incorrect. " in self.driver.page_source:
				self.logger.error("The Entered password is wrong.")
				sys.exit(0)
		except:
			sys.exit(0)

	def has_two_step(self):
		"""If there is two step auth returns False """
		self.login()
		try:
			WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'm0NAq')))
		except:
			return False

	def two_step_auth(self):
		if self.has_two_step() is False:
			n = input('Please enter the code that Instagram sent you: ')
			self.driver.find_element_by_xpath('//*[@class="_2hvTZ pexuQ zyHYP"]').send_keys(n)
			self.driver.find_element_by_xpath(
				'//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]').click()
			WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'mt3GC')))
			self.saving_cookies()
			return True
		else:
			self.saving_cookies()

	def dismiss_offer(self):
		self.open_login_page()
		offer_elem = "//*[contains(text(), 'Get App')]"
		dismiss_elem = "//*[contains(text(), 'Not Now')]"
		try:
			dismiss_elem = self.driver.find_element_by_xpath(dismiss_elem).click()
		except:
			pass

	def open_profile(self):
		self.dismiss_offer()
		self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[3]/a').click()
		time.sleep(5)

	def open_following_tab(self):
		self.open_profile()
		self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
		time.sleep(3)


Credentials().open_following_tab()
