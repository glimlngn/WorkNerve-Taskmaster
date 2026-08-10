import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Folder where the browser will persist cookies/session between runs
PROFILE_DIR = os.path.abspath("./selenium_profile")

# Setup Chromium browser and go to worknerve.techoneglobal.com
WORKNERVE_URL = 'https://worknerve.techoneglobal.com/login'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--user-data-dir={PROFILE_DIR}")
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_options)
actions = ActionChains(driver)

driver.get(WORKNERVE_URL)
actions.send_keys(Keys.TAB * 3).send_keys(Keys.ENTER).perform()
time.sleep(5)
input_element = driver.find_element(By.CSS_SELECTOR, "[aria-label='My Tasks']")
input_element.send_keys(Keys.ENTER)
actions.send_keys(Keys.TAB * 13).send_keys(Keys.ENTER).perform()

input('BREAKPOINT: enter anything to close the browser')

# # Get task list from Excel file
# path = 'worknerve_tasks_aug3_aug4.xlsx'
# task_list = pd.read_excel(path)
# input_element = driver.find_element(By.ID, '_r_1f_')
# input_element.send_keys('Hello World')

driver.quit()

# def add_task(task):
#     return

# for index, task in task_list.iterrows():
#     add_task(task)