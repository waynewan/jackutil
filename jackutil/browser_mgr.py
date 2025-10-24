from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import platform
import argparse
import datetime
import getpass
import hashlib
import os
import pandas as pd
import pickle
import sys
import tempfile
import time
import locale
from pprint import pprint
locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

CHROME_BINARY_LOCATION='/usr/bin/google-chrome'
CHROME_WEBDRIVER_BINARY_LOCATION='/usr/bin/chromedriver'

def create_new_browser(rootdir=None,persist_name=None,incognito=True,driver_bin_loc=CHROME_WEBDRIVER_BINARY_LOCATION,browser_bin_loc=CHROME_BINARY_LOCATION):
	params = locals().copy()
	un = platform.uname()
	if(un.system=="Linux"):
		return __create_new_browser_linux(**params)
	elif(un.system=="Windows"):
		return __create_new_chrome_win11(**params)
		# return __create_new_edge_win11(**params)
	raise ValueError(f"Do not know what to do with system type: {un.system}")

def __create_new_browser_linux(rootdir=None,persist_name=None,incognito=True,driver_bin_loc=CHROME_WEBDRIVER_BINARY_LOCATION,browser_bin_loc=CHROME_BINARY_LOCATION):
	if(rootdir is None):
		rootdir = tempfile.TemporaryDirectory()
	options = webdriver.ChromeOptions()
	options.binary_location = browser_bin_loc
	options.add_argument("user-data-dir=%s" % rootdir)
	options.add_experimental_option("prefs", {
		"download.default_directory":"%s/download/" % rootdir,
		"profile.default_content_setting_values.notifications" : 2
	})
	options.add_argument("--start-maximized")
	# -- ---------------------------------------------------------------------
	# !! try to avoid being detected as automated session
	# -- ---------------------------------------------------------------------
	# -- ---------------------------------------------------------------------
	# !! based on idea from (doesn't work)
	# !! https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver
	# !!
	# options.add_argument("user-agent=Chrome")
	# -- ---------------------------------------------------------------------
	# -- ---------------------------------------------------------------------
	# !! based on idea from (working)
	# !! https://piprogramming.org/articles/How-to-make-Selenium-undetectable-and-stealth--7-Ways-to-hide-your-Bot-Automation-from-Detection-0000000017.html
	# !! TDA: working as of 2022-03-17
	# !! fidelity: working as of 2022-03-17
	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option('useAutomationExtension', False)
	options.add_argument('--disable-blink-features=AutomationControlled')
	pprint(options)
	# -- ---------------------------------------------------------------------
	# --
	# --
	# --
	if(incognito):
		options.add_argument("--incognito")
	driver = webdriver.Chrome(options=options,executable_path=driver_bin_loc)
	if(persist_name is not None):
		persist_connection_info(driver=driver,persist_name=persist_name)
	return driver

def __create_new_chrome_win11(rootdir=None,persist_name=None,incognito=True,driver_bin_loc=CHROME_WEBDRIVER_BINARY_LOCATION,browser_bin_loc=CHROME_BINARY_LOCATION):
	if(rootdir is None):
		rootdir = tempfile.TemporaryDirectory()
	options = webdriver.ChromeOptions()
	options.add_argument("--start-maximized")
	# -- ---------------------------------------------------------------------
	# !! try to avoid being detected as automated session
	# -- ---------------------------------------------------------------------
	# -- ---------------------------------------------------------------------
	# !! based on idea from (doesn't work)
	# !! https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver
	# !!
	# options.add_argument("user-agent=Chrome")
	# -- ---------------------------------------------------------------------
	# -- ---------------------------------------------------------------------
	# !! based on idea from (working)
	# !! https://piprogramming.org/articles/How-to-make-Selenium-undetectable-and-stealth--7-Ways-to-hide-your-Bot-Automation-from-Detection-0000000017.html
	# !! TDA: working as of 2022-03-17
	# !! fidelity: working as of 2022-03-17
	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option('useAutomationExtension', False)
	options.add_argument('--disable-blink-features=AutomationControlled')
	pprint(options)
	# -- ---------------------------------------------------------------------
	# --
	# --
	# --
	if(incognito):
		options.add_argument("--incognito")
	driver = webdriver.Chrome(options=options)
	return driver

def __create_new_edge_win11(rootdir=None,persist_name=None,incognito=True,driver_bin_loc=CHROME_WEBDRIVER_BINARY_LOCATION,browser_bin_loc=CHROME_BINARY_LOCATION):
	from selenium.webdriver.edge.options import Options
	from selenium.webdriver.edge.service import Service
	# --
	options = Options()
	options.add_argument("--disable-blink-features=AutomationControlled")
	driver = webdriver.Edge(service=Service(), options=options)
	return driver

def persist_connection_info(*,driver=None,sessionURL=None,sessionID=None,persist_name):
	if(driver is not None):
		sessionURL = driver.command_executor._url
		sessionID = driver.session_id
	connection_info = {
		'url' : sessionURL,
		'session_id' : sessionID,
		'persist_name' : persist_name,
		'timestamp' : datetime.datetime.now()
	}
	fname = connection_info_name(persist_name)
	pickle.dump(connection_info,open(fname,"wb"))
	os.chmod(fname, 0o600) # only user can read/write

def temporary_dir_name(persist_name):
	hasher = hashlib.sha256()
	cinfo_name = "ci_{}".format(persist_name)
	hasher.update(cinfo_name.encode("utf-8"))
	return hasher.hexdigest()

def connection_info_name(persist_name):
	#hasher = hashlib.sha256()
	#cinfo_name = "ci_{}".format(persist_name)
	#hasher.update(cinfo_name.encode("utf-8"))
	hash = temporary_dir_name(persist_name)
	fname = f".{hash}.pk"
	return fname

def reconnect_browser(*,persist_name):
	fname = connection_info_name(persist_name)
	connection_info = pickle.load(open(fname,"rb"))
	driver = webdriver.Remote(command_executor=connection_info['url'],desired_capabilities={})
	driver.close() #// Remote will open a new browser
	driver.session_id = connection_info['session_id']
	return driver

