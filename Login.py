from selenium import webdriver
from selenium.webdriver.common.by import By
from getpass import getpass
import time

def login_to_SIS(driver):
    
    url = "https://student.msu.edu/splash.html"
    driver.get(url)
    
    element = driver.find_element(By.ID, 'loginUrl1') # Hit the login button
    element.click() 
    time.sleep(2)

    element = driver.find_element(By.ID, 'input28') # Find the MSU email input
    if not element.get_attribute('value'):
        print("Please enter your MSU email: ")
        email = input()
        element.send_keys(email)
        
    element = driver.find_element(By.ID, 'input36') # Find the password input
    print("Please enter your password: ")
    password = getpass()
    element.send_keys(password)
    
    element = driver.find_element(By.CLASS_NAME, 'o-form-button-bar') # Click Sign in
    element.click()
    time.sleep(5)
    
    buttons = driver.find_elements(By.CLASS_NAME, 'authenticator-button')
    for button in buttons:
        if button.get_attribute('data-se') == 'phone_number':
            button.click() # Click on authenticate by phone
    time.sleep(3)
    
    element = driver.find_element(By.TAG_NAME, 'input')  
    element.click() # Click on Receive code via SMS
    time.sleep(3)
    
    element = driver.find_element(By.TAG_NAME, "input") # Find the code input
    print("Please enter your SMS code: ")
    code = input()
    element.send_keys(code)
     
    element = driver.find_element(By.CLASS_NAME, 'o-form-button-bar') # Click Verify
    element.click()
    time.sleep(3)