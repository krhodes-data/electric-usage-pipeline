import time
from datetime import datetime, timedelta
import json
import glob
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains

webpage = 'https://www.sce.com/'

# Temporary credential protection
credPath = 'creds.json'
with open(credPath) as c:
    creds = json.load(c)
username = creds['username']
password = creds['password']

# To and from dates; formmated for text input on SCE website
# dates are the currently the same as it will pull just the singular day that way
fromDateFull = datetime.date(datetime.now()) - timedelta(days=1) # yesterday
fromDate = fromDateFull.strftime("%m%d%y")
toDateFull = datetime.date(datetime.now()) - timedelta(days=1) # also yesterday
toDate = toDateFull.strftime("%m%d%y")


def download_csv_raw(fromDate,toDate):
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)

    # Open page and login
    driver.get(webpage)
    driver.find_element(By.XPATH,
        '//*[@id="userName"]'
    ).send_keys(username)
    time.sleep(1)
    driver.find_element(By.XPATH,
        '//*[@id="password"]'
    ).send_keys(password)
    time.sleep(1)
    driver.find_element(By.XPATH,
        '//*[@id="HomeLoginButton"]'
    ).click()
    time.sleep(10)

    # Navigating to download prompt
    driver.find_element(By.XPATH,
        '/html/body/div/div[2]/div/aside/div[1]/div/nav/div[2]/div[2]/div[2]/a[5]'
    ).click()
    time.sleep(5)
    driver.find_element(By.XPATH,
        '/html/body/div/div[2]/div/section[2]/div/section[3]/div/article/div/section/div/div[2]/div/div[1]/section/user-based-datadownload-content/div/div/div[1]/div/div/div/div[2]/a'
    ).click()
    time.sleep(5)
    driver.find_element(By.XPATH,
        '/html/body/div/div[2]/div/section[2]/div/section[3]/div/article/div/section/div/div/div/div[1]/section/datadownload-content/div/div/div/section/div/div[2]/div[4]/div[2]/div/div/div[1]/div/div[2]'
    ).click()
    time.sleep(5)
    driver.find_element(By.XPATH,
        '//*[@id="fromDateTextBox"]'
    ).send_keys(fromDate)
    time.sleep(1)
    driver.find_element(By.XPATH,
        '//*[@id="toDateTextBox"]'
    ).send_keys(toDate)
    time.sleep(1)
    driver.find_element(By.XPATH,
        '/html/body/div[1]/div[2]/div/section[2]/div/section[3]/div/article/div/section/div/div/div/div[1]/section/datadownload-content/div/div/div/section/div/div[2]/div[3]/div[2]/fieldset/ul/li[1]/div/label/small'
    ).click()

    #WORKING AROUND CAPTCHA
    #BORROWED FROM https://gist.github.com/miodeqqq/b416b42e1573e6d35f464375297a070c
    #WHICH DEMONSTRATED THIS ON THE GOOGLE DEMO API FOR RECAPTCHA
    #BELOW WORKS FINE WHEN NOT PROMPTED BY "SELECT THE..." CAPTCHA - ABOUT 1 IN 3 TIMES
    #THIS MIGHT BE TRIGGERED BY THE FREQUENCY THAT THE SCRIPT IS CALLED,
    #SO IF THIS ONLY RUNS ONCE A DAY WE MIGHT BE ALRIGHT
    # find iframe
    captcha_iframe = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(
            (By.TAG_NAME, 'iframe')))
    time.sleep(1)
    ActionChains(driver).move_to_element(captcha_iframe).click().perform()
    time.sleep(10)
    '''
    # click im not robot
    captcha_box = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(
            (
                #By.ID, 'g-recaptcha-response' #original from snippet
                By.ID, 'recaptcha-anchor'
            )))
    '''
    time.sleep(1)
    # Return to main frame to access remaining elements
    driver.switch_to.default_content()
    time.sleep(1)
    driver.find_element(By.XPATH,
        '//*[@id="dataDownload"]'
    ).click()
    time.sleep(5)
    driver.find_element(By.XPATH,
    '//*[@id="dropdownLink2"]'
    ).click()
    time.sleep(1)
    driver.find_element(By.XPATH,
    '/html/body/div[1]/div[2]/div/section[1]/div[1]/div/section/react-header-login/div/section/div[4]/button/span'
    ).click()
    time.sleep(5)

    #driver.close()
    driver.quit()

# Verify file was downloaded

    keyword = "SCE_Usage"
    downloadPath = '/Users/kevinrhodes/Downloads/'
    files = glob.glob(downloadPath+"*.csv")
    latestFile = os.path.basename(max(files, key=os.path.getctime))
    for file in files:
        print(file)
    print(latestFile)




# Run script for testing
download_csv_raw(fromDate,toDate)


'''
#Basic Selenium:
driver = webdriver.Firefox()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
'''