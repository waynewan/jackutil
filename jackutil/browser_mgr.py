from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import subprocess
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

# ----------------------------------------------------------------------
# start browser in debug mode, but detached
# ----------------------------------------------------------------------
DEF_EDGE_BROWSER_PATH=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
DEF_EDGE_WEBDRV_PATH=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe"
DEF_CHROME_BROWSER_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
DEF_CHROME_WEBDRV_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
DEF_DEBUG_PORT = 9222
DEF_CHROME_USER_DATA_DIR=r"C:\temp\w11\chrome"
DEF_EDGE_USER_DATA_DIR=r"C:\temp\w11\edge"
# ----------------------------------------------------------------------
# Core Function
# ----------------------------------------------------------------------
def detach_process_flags():
	un = platform.uname()
	if(un.system=="Linux"):
		return {
			"stdout" : subprocess.DEVNULL,  # Redirect stdout to /dev/null
			"stderr" : subprocess.DEVNULL,  # Redirect stderr to /dev/null
			"stdin" : subprocess.DEVNULL,   # Redirect stdin from /dev/null
			"close_fds" : True,			 # Close all file descriptors
			"start_new_session" : True	  # Detach from the parent process group
		}
	elif(un.system=="Windows"):
		return {
			"stdout" : subprocess.DEVNULL,
			"stderr" : subprocess.DEVNULL,
			"close_fds" : True, 
			"creationflags" : subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
		}

def start_edge_for_debug(port=DEF_DEBUG_PORT, user_data_dir=DEF_EDGE_USER_DATA_DIR, edge_path=DEF_EDGE_BROWSER_PATH):
	# --
	# -- Ensure the user data directory exists
	# --
	os.makedirs(user_data_dir, exist_ok=True)
	# --
	# -- Construct the full list of command arguments
	# --
	command = [
		edge_path,
		f"--remote-debugging-port={port}",
		f"--user-data-dir={user_data_dir}",
		# Optional: Start with a clean slate for the UI 
		# "--disable-extensions",
		# "--disable-default-apps"
	]
	try:
		display(f"Starting chrome browser ... ")
		display(command)
		# --
		# -- Use subprocess.Popen to start the process
		# -- subprocess.DETACHED_PROCESS is a Windows-specific flag that ensures 
		# -- the process is fully independent.
		# --
		proc = subprocess.Popen(
			command,
			# Critical for detachment: Redirect stdout/stderr to a null device 
			# to prevent the Python parent process from blocking on I/O.
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
			close_fds=True, 
			creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
		)
		print(f"Edge started successfully. Process ID (PID): {proc.pid}")
		print(f"Debug Port: {port}, User Dir: {user_data_dir}")
		return proc

	except FileNotFoundError:
		print(f"ERROR: Edge executable not found: {edge_path}")
		raise e
	except Exception as e:
		print(f"ERROR starting process: {e}")
		raise e

def start_chrome_for_debug( port=DEF_DEBUG_PORT, user_data_dir=DEF_CHROME_USER_DATA_DIR, chrome_path=DEF_CHROME_BROWSER_PATH):
	# --
	# -- Ensure the user data directory exists for the isolated profile
	# --
	os.makedirs(user_data_dir, exist_ok=True)
	# --
	# -- Construct the full list of command arguments
	# --
	command = [
		chrome_path,
		f"--remote-debugging-port={port}",
		f"--user-data-dir={user_data_dir}",
		# Optional: Start with a clean slate for the UI 
		# "--disable-extensions",
		# "--disable-default-apps"
	]
	try:
		display(f"Starting chrome browser ... ")
		display(command)
		# --
		# -- Use subprocess.Popen to start the process
		# -- The creationflags ensure the process is fully independent (detached)
		# --
		proc = subprocess.Popen(
			command,
			**detach_process_flags(),
		)
		print(f"Chrome started successfully. Process ID (PID): {proc.pid}")
		print(f"Debug Port: {port}, User Dir: {user_data_dir}")
		return proc
	except FileNotFoundError:
		print(f"ERROR: Chrome executable not found: {chrome_path}")
		raise e
	except Exception as e:
		print(f"ERROR starting process: {e}")
		raise e

def start_browser_for_debug(port=DEF_DEBUG_PORT, user_data_dir=DEF_CHROME_USER_DATA_DIR, browser_type="chrome", browserPath=DEF_CHROME_BROWSER_PATH):
	if(browser_type=="chrome"):
		return start_chrome_for_debug(
			port=port, 
			user_data_dir=user_data_dir, 
			chrome_path=browserPath
		)
	elif(browser_type=="edge"):
		return start_edge_for_debug(
			port=port, 
			user_data_dir=user_data_dir, 
			edge_path=browserPath
		)
	else:
		raise ValueError(f"browser_type must be 'chrome' and 'edge'")

# --
# --
# --
def connect_to_edge_browser(port=DEF_DEBUG_PORT, driverPath=DEF_EDGE_WEBDRV_PATH):
	from selenium.webdriver.edge.options import Options
	from selenium.webdriver.edge.service import Service
	# --
	# --- Setup Options ---
	# --
	edge_options = Options()
	# --
	# -- THE CRITICAL STEP:
	# -- This tells Selenium: "Don't open a new window. 
	# -- Look for an existing browser listening on this address."
	# --
	edge_options.add_experimental_option("debuggerAddress", f"localhost:{port}")
	try:
		print(f"Connecting to Edge on port {port}...")
		print(f"driver binary {driverPath}...")
		# --
		service = Service(executable_path=driverPath)
		driver = webdriver.Edge(service=service, options=edge_options)
		# --
		# -- Prove the connection works by printing the current page title
		# --
		print("Successfully connected!")
		print(f"Current Page Title: {driver.title}")
		return driver
	except Exception as e:
		print(f"Connection failed: {e}")
		raise e

def connect_to_chrome_browser(port=DEF_DEBUG_PORT, driverPath=DEF_CHROME_WEBDRV_PATH):
	from selenium.webdriver.chrome.service import Service
	from selenium.webdriver.chrome.options import Options
	# --
	# --- Setup Options ---
	# --
	chrome_options = Options()
	# --
	# -- THE CRITICAL STEP:
	# -- This tells Selenium: "Don't open a new window.
	# -- Look for an existing browser listening on this address."
	# --
	chrome_options.add_experimental_option("debuggerAddress", f"localhost:{port}")
	# --- Connect ---
	try:
		print(f"Using ChromeDriver binary from: {driverPath}...")
		print(f"Connecting to Chrome on port {port}...")
		# --
		# -- Initialize the Service object with the ChromeDriver path
		# --
		service = Service(executable_path=driverPath)
		driver = webdriver.Chrome(service=service, options=chrome_options)
		# --
		# -- Prove the connection works by printing the current page title
		# --
		print("Successfully connected!")
		print(f"Current Page Title: {driver.title}")
		return driver
	except Exception as e:
		print(f"Connection failed: {e}")
		raise e

def connect_to_browser(port=DEF_DEBUG_PORT, browser_type=None, driverPath=DEF_EDGE_WEBDRV_PATH):
	if(browser_type=="chrome"):
		return connect_to_chrome_browser(
			port=port, 
			driverPath=driverPath
		)
	elif(browser_type=="edge"):
		return connect_to_edge_browser(
			port=port, 
			driverPath=driverPath
		)
	else:
		raise ValueError(f"browser_type must be 'chrome' and 'edge'")

# --
# --
# --
def is_driver_connected(driver):
	try:
		# Attempt to access a property that requires an active session
		current_url = driver.current_url 
		print(f"Driver is connected. Current URL: {current_url}")
		return True
	except WebDriverException as e:
		print(f"Driver is DISCONNECTED or session is invalid.")
		print(f"Error: {e.__class__.__name__}")
		return False
	except Exception as e:
		# Catch unexpected errors (e.g., driver object is None)
		print(f"An unexpected error occurred: {e}")
		return False

# --
# --
# --
def temporary_dir_name(persist_name):
	hasher = hashlib.sha256()
	cinfo_name = "ci_{}".format(persist_name)
	hasher.update(cinfo_name.encode("utf-8"))
	return hasher.hexdigest()

