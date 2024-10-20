from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
import time

def get_driver(choice):
    '''
    Initialize a Selenium WebDriver based on choice.

    Parameters:
    choice (str): The name of the browser to use. Options are 'Chrome' or 'Firefox'.

    Returns:
    WebDriver: An instance of the specified WebDriver (Chrome or Firefox). 
                If the driver cannot be started in normal mode, it falls back to headless mode.
                Returns None if the choice is not recognized.

    Notes:
    - The function attempts to start the driver in regular mode first. 
    - If there is an error starting the driver, it will attempt to start it in headless mode.
    '''
    if choice == 'Chrome':
        opts = webdriver.ChromeOptions()
        try: # Try starting a regular driver
            driver = webdriver.Chrome(options=opts)
        except: # If not possible, start a headless/invisible driver
            opts.add_argument("--headless")
            driver = webdriver.Chrome(options=opts)
            print('Headless/Invisible Driver')
        return driver
    if choice == 'Firefox': 
        opts = webdriver.FirefoxOptions()
        try: # Try starting a regular driver
            driver = webdriver.Firefox(options=opts)
        except: # If not possible, start a headless/invisible driver
            opts.add_argument("--headless")
            driver = webdriver.Firefox(options=opts)
            print('Headless/Invisible Driver')
        return driver
    return None
        
def login_to_SIS(driver, authenticate='Phone'):
    '''
    Login to MSU SIS with an authentication method of choice

    Parameters:
    driver: Initialized Selenium WebDriver.
    authenticate (str): The authentication method. Options are 'Phone' or 'Okta'. The default is 'Phone'.

    Notes: 
    - The function will ask for MSU NetID (netid@msu.edu), MSU password (it will be redacted)
    - Based on your authentication choice, either enter the received SMS code, 
      or the Okta Verify code in the app
    '''
    wait = WebDriverWait(driver, 20)
    url = "https://student.msu.edu/splash.html"
    driver.get(url) # Get to the MSU SIS Login screen
    wait.until(EC.element_to_be_clickable((By.ID , 'loginUrl1'))) # Wait until the Login button is clickable
    
    element = driver.find_element(By.ID, 'loginUrl1') 
    element.click() # Hit the login button
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'o-form-button-bar'))) 
    # Wait until the Sign in button is clickable

    element = driver.find_element(By.ID, 'input28') # Find the MSU email input
    element.clear() # Clear the email input
    print("Please enter your MSU email: ")
    email = input()
    element.send_keys(email) # Send input to email input box
        
    element = driver.find_element(By.ID, 'input36') # Find the password input
    print("Please enter your password: ")
    password = getpass()
    element.send_keys(password) # Send input to password input box
    
    element = driver.find_element(By.CLASS_NAME, 'o-form-button-bar') 
    element.click() # Click Sign in
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'authenticator-button'))) 
    # Wait until the first Select button is clickable
    
    buttons = driver.find_elements(By.CLASS_NAME, 'authenticator-button') # Get all button
    for button in buttons:
        if authenticate == 'Phone':
            if button.get_attribute('data-se') == "phone_number":
                button.click() # Click on authenticate by phone
                break
        if authenticate == 'Okta':
            if button.get_attribute('data-se') == "okta_verify-totp":
                button.click() # Click on authenticate by Okta code
                break
    
    element = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'input'))) 
    # Wait until the Receive code via SMS button is clickable
    element.click() # Click Receive code via SMS
    time.sleep(1) # More time to adjust
    
    element = driver.find_element(By.TAG_NAME, "input") # Find the code input
    if authenticate == 'Phone':    
        print("Please enter your SMS code: ")
    if authenticate == 'Okta':
        print("Please enter your Okta Verify code: ")
    code = input()
    element.send_keys(code) # Send input to code input box
     
    element = driver.find_element(By.CLASS_NAME, 'o-form-button-bar') 
    element.click() # Click Verify
    time.sleep(3)
    try: 
        element = wait.until(EC.element_to_be_clickable((By.ID, "PTNUI_LAND_REC_GROUPLET_LBL$1")))
        element.click() # Click on the Classes box
        time.sleep(3)
    except: # In case SIS take you to another Login screen
        element = wait.until(EC.element_to_be_clickable(By.ID, 'loginUrl1'))
        element.click() # Click on Login again
        element = wait.until(EC.element_to_be_clickable((By.ID, "PTNUI_LAND_REC_GROUPLET_LBL$1")))
        element.click() # Click on the Classes box
        time.sleep(3)
        
    try:
        element = driver.find_element(By.ID, 'SCC_LO_FL_WRK_SCC_VIEW_BTN$2')  
        driver.execute_script("arguments[0].click();", element) # Click on Class Search & Enroll
        wait.until(EC.element_to_be_clickable((By.ID, "DERIVED_SSR_FL_SSR_CSTRMPRV_GRP"))) 
        # Wait until the dropdown option "Term prior to..." is available 
    except:
        pass # If there's no Class Search & Enroll, proceed
    
    return None

def get_semesters_list(driver):
    '''
    Get a list of all semesters in MSU SIS

    Parameters:
    driver: Initialized Selenium WebDriver.

    Returns:
    semesters_list: a complete chronological list of all semesters in MSU SIS 
    previous_semesters: a list of previous semesters in MSU SIS (before now)

    Notes: 
    - The function scrapes for available current semesters and appends to current_semesters
    - The function will then click on the dropdown option to scrape for previous semesters,
      and append to previous_semesters
    - The complete list of semesters is combined from current_semesters and previous_semesters
    '''
    wait = WebDriverWait(driver, 20)
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
    
    previous_semesters.reverse() # Reverse previous_semesters, it's in reverse chronological order
    semesters_list = list(dict.fromkeys(previous_semesters + current_semesters)) 
    # Get only the unique semesters from both lists
    return semesters_list, previous_semesters

def switch_to_semester(driver, semester, previous_semesters):
    '''
    Switch to a specified semester

    Parameters:
    driver: Initialized Selenium WebDriver.
    semester (str): The semester to switch to.
    previous_semesters: a list of previous semesters in MSU SIS (before now)
    
    Returns:
    str: A message indicating the result of the operation. 
         If the current semester is the same as the desired one, it returns 
         "No need to switch Semester". Otherwise, it confirms the switch.
    
    Notes:
    - The function checks the current semester displayed on the page.
    - If the current semester does not match the desired semester, it 
      triggers a JavaScript function to change the semester.
    - If the desired semester is in the list of previous semesters, 
      it clicks the dropdown element to access those options.
    '''
    wait = WebDriverWait(driver, 20)
    try: # Find the current semester displayed on the page
        cur_page = driver.find_element(By.ID, "TERM_VAL_TBL_DESCR").text
    except: # If not in any semester
        cur_page = None 

    if cur_page == semester.replace('Semester ', ''): # If already in the right semester
        return "No need to switch Semester"
        
    if cur_page and cur_page != semester.replace('Semester ', ''): # If not in the right semester
        change_semester = "javascript:submitAction_win9(document.win9,'DERIVED_SSR_FL_SSR_CHANGE_BTN');"
        driver.execute_script(change_semester); # Click change term
        wait.until(EC.frame_to_be_available_and_switch_to_it(0)) # Wait for popup iframe and switch to it
        wait.until(EC.element_to_be_clickable((By.ID, "DERIVED_SSR_FL_SSR_CSTRMPRV_GRP"))) 
        # Wait until the dropdown 'Terms prior to...' is clickable
    
    if semester in previous_semesters: # If the desired semester is a previous semester
        element = driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_CSTRMPRV_GRP")
        element.click() # Click on 'Terms prior to ...'
        time.sleep(1)
    element = driver.find_element(By.LINK_TEXT, semester) 
    driver.execute_script("arguments[0].click();", element) # Click on the desired semester
    time.sleep(2)
    
    driver.switch_to.default_content() # Switch back to the main page
    time.sleep(1)
    return f"Switch to {semester}"