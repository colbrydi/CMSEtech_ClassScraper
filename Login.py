from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
import time

def get_driver(choice):
    if choice == 'Chrome':
        opts = webdriver.ChromeOptions()
        try: 
            driver = webdriver.Chrome(options=opts)
        except:
            opts.add_argument("--headless")
            driver = webdriver.Chrome(options=opts)
            print('Headless/Invisible Driver')
        return driver
    if choice == 'Firefox':
        opts = webdriver.FirefoxOptions()
        try: 
            driver = webdriver.Firefox(options=opts)
        except:
            opts.add_argument("--headless")
            driver = webdriver.Firefox(options=opts)
            print('Headless/Invisible Driver')
        return driver
    return None
        
def login_to_SIS(driver, authenticate='Phone'):
    wait = WebDriverWait(driver, 10)
    url = "https://student.msu.edu/splash.html"
    driver.get(url)
    wait.until(EC.element_to_be_clickable((By.ID , 'loginUrl1'))) # Wait until the Login button is clickable
    
    element = driver.find_element(By.ID, 'loginUrl1') # Hit the login button
    element.click() 
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'o-form-button-bar'))) # Wait until the Sign in button is clickable

    element = driver.find_element(By.ID, 'input28') # Find the MSU email input
    element.clear()
    print("Please enter your MSU email: ")
    email = input()
    element.send_keys(email)
        
    element = driver.find_element(By.ID, 'input36') # Find the password input
    print("Please enter your password: ")
    password = getpass()
    element.send_keys(password)
    
    element = driver.find_element(By.CLASS_NAME, 'o-form-button-bar') # Click Sign in
    element.click()
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'authenticator-button'))) # Wait until the first Select button is clickable
    
    buttons = driver.find_elements(By.CLASS_NAME, 'authenticator-button') # Get all button
    for button in buttons:
        if authenticate == 'Phone':
            if button.get_attribute('data-se') == "phone_number":
                button.click() # Click on authenticate by phone
                break
        if authenticate == 'Okta':
            if button.get_attribute('data-se') == "okta_verify-totp":
                button.click() # Click on authenticate by phone
                break
    
    element = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'input'))) # Wait until the Receive code via SMS button is clickable
    element.click() # Click Receive code via SMS
    time.sleep(1)
    
    element = driver.find_element(By.TAG_NAME, "input") # Find the code input
    if authenticate == 'Phone':    
        print("Please enter your SMS code: ")
    if authenticate == 'Okta':
        print("Please enter your Okta Verify code: ")
    code = input()
    element.send_keys(code)
     
    element = driver.find_element(By.CLASS_NAME, 'o-form-button-bar') # Click Verify
    element.click()
    time.sleep(3)
    try: 
        element = wait.until(EC.element_to_be_clickable((By.ID, "PTNUI_LAND_REC_GROUPLET_LBL$1")))
        element.click()
        time.sleep(3)
    except:
        element = wait.until(EC.element_to_be_clickable(By.ID, 'loginUrl1'))
        element.click()
        element = wait.until(EC.element_to_be_clickable((By.ID, "PTNUI_LAND_REC_GROUPLET_LBL$1")))
        element.click()
        time.sleep(3)
        
    try:
        element = driver.find_element(By.ID, 'SCC_LO_FL_WRK_SCC_VIEW_BTN$2')  # Click on Class Search & Enroll
        driver.execute_script("arguments[0].click();", element)
        wait.until(EC.element_to_be_clickable((By.ID, "DERIVED_SSR_FL_SSR_CSTRMPRV_GRP")))
    except:
        pass # If there's no Class Search & Enroll, proceed
    
    return None

def get_semesters_list(driver):
    wait = WebDriverWait(driver, 10)
    current_semesters = []
    current_cells = driver.find_elements(By.XPATH, "//tr[@class='ps_grid-row psc_rowact']")
    for cell in current_cells: # Find each semester's ID
        semester = cell.find_element(By.XPATH, ".//a[@class='ps-link']")
        if semester.text != '':
            current_semesters.append(semester.text)
    
    element = driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_CSTRMPRV_GRP")
    element.click() # Click on 'Terms prior to ...'
    time.sleep(1)
    
    previous_semesters = []
    previous_cells = driver.find_elements(By.XPATH, "//tr[@class='ps_grid-row psc_rowact']")
    for cell in previous_cells: # Find each semester's ID
        semester = cell.find_element(By.XPATH, ".//a[@class='ps-link']")
        if semester.text != '':
            previous_semesters.append(semester.text)
    
    element = driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_CSTRMPRV_GRP")
    element.click() # Click on 'Terms prior to ...'
    time.sleep(1)
    
    previous_semesters.reverse()
    semesters_list = previous_semesters + current_semesters
    return semesters_list, previous_semesters, current_semesters

def switch_to_semester(driver, semester, previous_semesters):
    wait = WebDriverWait(driver, 10)
    try:
        cur_page = driver.find_element(By.ID, "TERM_VAL_TBL_DESCR").text
    except:
        cur_page = None 

    if cur_page == semester.replace('Semester ', ''):
        return "No need to switch Semester"
        
    if cur_page and cur_page != semester.replace('Semester ', ''):
        change_semester = "javascript:submitAction_win9(document.win9,'DERIVED_SSR_FL_SSR_CHANGE_BTN');"
        driver.execute_script(change_semester);
        wait.until(EC.frame_to_be_available_and_switch_to_it(0))
        wait.until(EC.element_to_be_clickable((By.ID, "DERIVED_SSR_FL_SSR_CSTRMPRV_GRP")))
    
    if semester in previous_semesters: 
        element = driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_CSTRMPRV_GRP")
        element.click() # Click on 'Terms prior to ...'
        time.sleep(1)
    element = driver.find_element(By.LINK_TEXT, semester)
    driver.execute_script("arguments[0].click();", element)
    time.sleep(2)
    
    driver.switch_to.default_content()
    time.sleep(1)
    return f"Switch to {semester}"