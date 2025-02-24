from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

SCHOOL_NAME = "Brown University"
SSO_Username = "yqiu35"
SSO_Password = "Jimmy3939:"
# execution_num = 2*60*60/15 
execution_num = 10

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Open Top Hat login page
    driver.get("https://app.tophat.com/login")
    print("opening tophat login page")

    # Enter Brown University
    school_input = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search for your school']"))
    )
    school_input.send_keys(SCHOOL_NAME)
    time.sleep(2)  

    school_input.send_keys(Keys.DOWN)  
    school_input.send_keys(Keys.RETURN)

     # Click login with school button
    login_with_school_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-click-id="sso login button"]'))
    )
    login_with_school_button.click()
    print("Clicked 'Log in with school account'.")

    # Detect sso page
    WebDriverWait(driver, 1).until(
        EC.url_contains("sso.brown.edu/idp/profile/SAML2/Redirect/SSO")
    )
    print("Redirected to Brown University SSO.")

    # SSO Enter username and Password
    netid_field = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.NAME, "j_username"))
    )
    netid_field.send_keys(SSO_Username)

    password_field = driver.find_element(By.NAME, "j_password")
    password_field.send_keys(SSO_Password + Keys.RETURN)
    print("Pass SSO.")

    # press trust the device
    trust_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "trust-browser-button"))
    )
    trust_button.click()

    # check url inside tophat
    WebDriverWait(driver, 2).until(
        EC.url_contains("app.tophat.com/e")
    )
    print("Inside Tophat")

    # click on enter course button
    enter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Enter']]")))
    enter_button.click()
    print("Clicked 'Enter' button for the course.")

    # check url inside course
    WebDriverWait(driver, 10).until(
        EC.url_contains("app.tophat.com/e/895328/content/course-work")
    )
    print("Inside Course")

    # click the classroom 
    classroom_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-click-id='nav tab lecture']")))
    classroom_tab.click()
    print("Clicked 'Classroom' tab.")

    # refresh until question comes up
    send_count = 0
    while (send_count < execution_num):
        driver.refresh()
        time.sleep(15)
finally:
    # 关闭浏览器
    time.sleep(10)
    driver.quit()