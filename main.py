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
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={PROFILE_DIR}")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)
actions = ActionChains(driver)
driver.get(WORKNERVE_URL)

# Assuming auth retented, go to 'My Tasks' and hover on the '+ Add Task' button.
actions.send_keys(Keys.TAB * 3).send_keys(Keys.ENTER).perform()
time.sleep(3)
input_element = driver.find_element(By.CSS_SELECTOR, "[aria-label='My Tasks']")
input_element.send_keys(Keys.ENTER)
time.sleep(1)
actions.send_keys(Keys.TAB * 13).perform()

# input('BREAKPOINT: press ENTER to continue.')

# Get task list from Excel file
path = 'test_file.xlsx'
task_list = pd.read_excel(path)

# Press 'Add Task'
actions.send_keys(Keys.ENTER).perform()
actions.send_keys(Keys.TAB * 5).perform()

# TODO: Loop through all tasks in the Excel file
task_index = 8
# Input Task Data
# Service Line
actions.send_keys(task_list.iloc[task_index]['service_line']).perform()
time.sleep(0.3)
actions.send_keys(Keys.ARROW_DOWN, Keys.ENTER, Keys.TAB).perform()

# Category
actions.send_keys(task_list.iloc[task_index]['category']).perform()
time.sleep(0.3)
actions.send_keys(Keys.ARROW_DOWN, Keys.ENTER, Keys.TAB).perform()

# Sub-category
actions.send_keys(task_list.iloc[task_index]['subcategory']).perform()
time.sleep(0.3)
actions.send_keys(Keys.ARROW_DOWN, Keys.ENTER, Keys.TAB).perform()

# Project/Program/Managed Service (for manual input)
with_oppo = task_list.iloc[task_index]['with_oppo']
if(with_oppo == 'Yes'):
    actions.send_keys('').perform()
    time.sleep(0.3)
    actions.send_keys(Keys.ARROW_DOWN, Keys.ENTER, Keys.TAB).perform()
elif(with_oppo == 'Sometimes'): 
    actions.send_keys(Keys.TAB).perform()
elif(with_oppo == 'No'):
    pass

# Task Title
actions.send_keys(task_list.iloc[task_index]['task_title']).perform()
time.sleep(0.3)
actions.send_keys(Keys.ARROW_DOWN, Keys.ENTER, Keys.TAB).perform()

# Description
actions.send_keys(task_list.iloc[task_index]['description']).perform()
time.sleep(0.3)
actions.send_keys(Keys.ARROW_DOWN, Keys.ENTER, Keys.TAB).perform()

# TODO: automate Priority selection
actions.send_keys(Keys.TAB).perform()
# actions.send_keys(task_list.iloc[task_index]['priority']).perform()
# time.sleep(0.3)
# actions.send_keys(Keys.ARROW_DOWN, Keys.ENTER, Keys.TAB).perform()

# Estimated Hours
actions.send_keys(task_list.iloc[task_index]['estimated_hours']).perform()
time.sleep(0.3)
actions.send_keys(Keys.ENTER).perform()
actions.send_keys(Keys.ENTER, Keys.TAB, Keys.TAB).perform()

# Add Task to WorkNerve
actions.send_keys(Keys.ENTER).perform()
time.sleep(3)

# Press '+ Add Task' and move to Service Line
actions.send_keys(Keys.ENTER).perform()
actions.send_keys(Keys.TAB * 5).perform()

input('BREAKPOINT: press ENTER to continue.')

driver.quit()