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
time.sleep(3)
actions.send_keys(Keys.TAB * 3).send_keys(Keys.ENTER).perform()
time.sleep(3)

input('Have you logged-in? Please press ENTER to continue. ')

input_element = driver.find_element(By.CSS_SELECTOR, "[aria-label='My Tasks']")
input_element.send_keys(Keys.ENTER)

input('Please select a date, and press ENTER to start adding tasks. ')

# Assuming auth retented, go to 'My Tasks' and hover on the '+ Add Task' button.
# input('BREAKPOINT: press ENTER to continue. ')
input_element = driver.find_element(By.CSS_SELECTOR, "[aria-label='My Tasks']")
input_element.send_keys(Keys.ENTER)
time.sleep(0.5)
actions.send_keys(Keys.TAB * 13).perform()
time.sleep(0.5)

# Get task list from Excel file
# path = "C:/Users/TOG-PH/OneDrive - Tech One Global Singapore Pte. Ltd/Documents/Copilot/Created/WorkNerve_Tasks_20260814.xlsx"
path = "test_file.xlsx"
task_list = pd.read_excel(path)

# Input Task Data
for _, task in task_list.iterrows(): 
    # Press '+ Add Task' and move to Service Line
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(0.5)
    actions.send_keys(Keys.TAB * 5).perform()
    time.sleep(0.5)
    # Service Line
    actions.send_keys(task['service_line']).perform()
    time.sleep(0.5)
    actions.send_keys(Keys.ARROW_DOWN, Keys.ENTER, Keys.TAB).perform()

    # Category
    actions.send_keys(task['category']).perform()
    time.sleep(0.5)
    actions.send_keys(Keys.ARROW_DOWN, Keys.ENTER, Keys.TAB).perform()

    # Sub-category
    actions.send_keys(task['subcategory']).perform()
    time.sleep(0.5)
    actions.send_keys(Keys.ARROW_DOWN, Keys.ENTER, Keys.TAB).perform()

    # Project/Program/Managed Service (for manual input)
    with_oppo = task['with_oppo']
    if(with_oppo == 'Yes'):
        actions.send_keys(' ').perform()
        time.sleep(0.5)
        actions.send_keys(Keys.ARROW_DOWN, Keys.ENTER, Keys.TAB).perform()
    elif(with_oppo == 'Sometimes'): 
        actions.send_keys(Keys.TAB).perform()
    elif(with_oppo == 'No'):
        pass

    # Task Title
    actions.send_keys(task['task_title']).perform()
    time.sleep(0.5)
    actions.send_keys(Keys.ARROW_DOWN, Keys.ENTER, Keys.TAB).perform()

    # Description
    actions.send_keys(task['description']).perform()
    time.sleep(0.5)
    actions.send_keys(Keys.ARROW_DOWN, Keys.ENTER, Keys.TAB).perform()

    # Priority
    priority = task['priority']
    if(priority == 'Low'):
        actions.send_keys(Keys.ENTER, Keys.ARROW_UP, Keys.ENTER).perform()
    elif(priority == 'High'):
        actions.send_keys(Keys.ENTER, Keys.ARROW_DOWN, Keys.ENTER).perform()
    elif(priority == 'Urgent'): 
        actions.send_keys(Keys.ENTER, Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ENTER).perform()
        pass
    actions.send_keys(Keys.TAB).perform()

    # Estimated Hours
    actions.send_keys(str(task['estimated_hours'])).perform()
    time.sleep(0.5)
    actions.send_keys(Keys.ENTER).perform()
    actions.send_keys(Keys.ENTER, Keys.TAB, Keys.TAB).perform()

    # Add Task to WorkNerve
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(2)

input('Task tracking done. After selecting OPPO, please press ENTER to log time. ')

# Log Hours
added_tabs = 0 # increments by 4 per iteration, to go through the tasks
log_ctr = 0 # after 5 tasks logged, prompt user to turn to next page
for idx in reversed(task_list.index): # iterates in reverse. in logging hours, FI-LO
    if log_ctr % 5 == 0:
        added_tabs = 0
        input('All tasks logged for this page (or this is the first page lol). Please go to the next page. ')
    input_element = driver.find_element(By.CSS_SELECTOR, "[aria-label='My Tasks']")
    input_element.send_keys(Keys.ENTER)
    time.sleep(0.5)
    actions.send_keys(Keys.TAB * 16, Keys.TAB * added_tabs, Keys.ENTER).perform()
    time.sleep(0.5)
    actions.send_keys(Keys.TAB * 2).perform()
    time.sleep(0.5)
    actions.send_keys(str(task_list.loc[idx]['estimated_hours'])).perform()
    time.sleep(0.5)
    actions.send_keys(Keys.TAB * 3).send_keys(Keys.ENTER).perform()
    time.sleep(0.5)
    added_tabs += 4
    log_ctr += 1

# Complete Tasks
added_tabs = 0 # increments by 4 per iteration, to go through the tasks
log_ctr = 0 # after 5 tasks logged, prompt user to turn to next page
input('Hour logging done. Please press ENTER to complete tasks. ')
for _, task in task_list.iterrows(): 
    if log_ctr % 5 == 0:
        added_tabs = 0
        input('All tasks completed for this page (or this is the first page lol). Please go to the next page. ')
    input_element = driver.find_element(By.CSS_SELECTOR, "[aria-label='My Tasks']")
    input_element.send_keys(Keys.ENTER)
    time.sleep(0.5)
    actions.send_keys(Keys.TAB * 15, Keys.TAB * added_tabs, Keys.ENTER).perform()
    time.sleep(0.5)
    actions.send_keys(Keys.TAB * 6, Keys.ENTER).perform()
    time.sleep(0.5)
    added_tabs += 1
    log_ctr += 1

input('WorkNerve Taskmaster done. Please press ENTER to close the browser. ')
    
driver.quit()