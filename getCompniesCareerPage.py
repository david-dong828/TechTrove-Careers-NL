# Name: Dong Han
# Mail: dongh@mun.ca
import json,os
import time
from datetime import datetime
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import random
from urllib.parse import urlparse
import database_handle

def save_json(filePath, all_items):
    with open(filePath,"w") as f:
        json.dump(all_items,f)

def is_job_file_existed(companyName):
    today_date = datetime.now().strftime("%Y-%m-%d")
    fileName = companyName + "_" + today_date + ".json"

    foler = "temp"
    if not os.path.exists(foler):
        os.makedirs(foler)
    filePath = os.path.join(foler,fileName)

    if os.path.exists(filePath):
        return True, filePath
    else:
        return False, filePath

def seleniumDriver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
    options.add_argument("--headless")

    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def simulateHumanOperation(driver):
    # Random delay
    time.sleep(random.uniform(1, 3))
    # Simulate human-like mouse movements
    action = ActionChains(driver)
    action.move_to_element(driver.find_element(By.TAG_NAME, 'body')).perform()
    action.move_by_offset(random.randint(10, 100), random.randint(10, 100)).perform()

    # Wait for the page to load completely
    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: d.execute_script("return document.readyState === 'complete';"))

def checkVerafin(url):
    # If file already there, then stop and extract data
    company = "verafin"
    isjobFileExisted, filePath = is_job_file_existed(company)
    if isjobFileExisted:
        return filePath

    #connect MySQL
    db, cursor = database_handle.connectDB()
    database_handle.createTable(cursor)

    # Start scrape with Selenium
    driver = seleniumDriver()
    driver.get(url)

    simulateHumanOperation(driver)

    all_items = {}
    try:
        # product_element can get all stuff within <ul> as a whole, but we need each <li>, so its useless here
        # product_element = driver.find_element(By.CSS_SELECTOR,"#mainContent > div > div.css-uvpbop > section > ul")

        # get the <li> quantities within <ul>
        list_item_count = len(driver.find_elements(By.XPATH, "//*[@id='mainContent']/div/div[2]/section/ul/li"))
        # print(list_item_count)

        for i in range(1,list_item_count+1):
            item = driver.find_element(By.XPATH, f"//*[@id='mainContent']/div/div[2]/section/ul/li[{i}]")

            jobID= item.find_element(By.CSS_SELECTOR, "ul[data-automation-id='subtitle'] > li").text
            jobItemPart = item.find_element(By.CSS_SELECTOR,"h3 > a")
            all_items[jobID] = {
                "job_title":jobItemPart.text,
                "link":jobItemPart.get_attribute("href")
            }
            database_handle.saveTotable(company,jobItemPart.text,jobItemPart.get_attribute("href"),jobID,db,cursor)

        db.close()
        save_json(filePath, all_items)

        return filePath

    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.save_screenshot('debug_screenshot_after_timeout.png')
        return
    except NoSuchElementException:
        print("Could not find the elements within it.")
        return
    finally:
        driver.quit()

def checkColab(url):
    # If file already there, then stop and extract data
    company = "colab"
    isjobFileExisted, filePath = is_job_file_existed(company)
    if isjobFileExisted:
        return filePath

    # connect MySQL
    db, cursor = database_handle.connectDB()
    database_handle.createTable(cursor)

    # Start scrape with Selenium
    driver = seleniumDriver()
    driver.get(url)

    simulateHumanOperation(driver)

    all_items = {}
    try:
        # get the <li> quantities within <ul>
        list_item_count = len(driver.find_elements(By.XPATH, "//div[contains(@class, 'career-grid-list')]/a"))
        print(list_item_count)
        for i in range(1, list_item_count + 1):
            item = driver.find_element(By.XPATH, f"//div[contains(@class, 'career-grid-list')]/a[{i}]")
            jobLink = item.get_attribute("href")
            job_title = item.find_element(By.CSS_SELECTOR,"h6").text
            jobID = jobLink.split("/")[-1]
            all_items[jobID] = {
                "job_title": job_title,
                "link": jobLink
            }
            database_handle.saveTotable(company, job_title, jobLink, jobID, db, cursor)

        db.close()
        save_json(filePath, all_items)

        return filePath

    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.save_screenshot('debug_screenshot_after_timeout.png')
        return
    except NoSuchElementException:
        print("Could not find the elements within it.")
        return
    finally:
        driver.quit()
def main():
    # verafin_link = "https://nasdaq.wd1.myworkdayjobs.com/en-US/US_External_Career_Site?q=verafin"
    # jobFile = checkVerafin(verafin_link)
    # print(jobFile)

    colab_link = "https://www.colabsoftware.com/careers#openings"
    jobfile = checkColab(colab_link)
    print(jobfile)

    '''
    /html/body/div[3]/div[5]/div/div/div[1]/div
    /html/body/div[3]/div[5]/div/div/div[1]/div/a[1]
    /html/body/div[3]/div[5]/div/div/div[1]/div/a[2]
    /html/body/div[3]/div[5]/div/div/div[1]/div/a[1]/h6
    
    #w-node-_0efbb2ad-c225-2158-3f3c-f6195d0332d8-5d0332d5 > div > a:nth-child(1)
    //*[@id="w-node-_0efbb2ad-c225-2158-3f3c-f6195d0332d8-5d0332d5"]/div/a[1]
    //*[@id="w-node-_0efbb2ad-c225-2158-3f3c-f6195d0332d8-5d0332d5"]/div
    
    #w-node-_0efbb2ad-c225-2158-3f3c-f6195d0332d8-5d0332d5 > div
    document.querySelector("#w-node-_0efbb2ad-c225-2158-3f3c-f6195d0332d8-5d0332d5 > div")
    //*[@id="w-node-_0efbb2ad-c225-2158-3f3c-f6195d0332d8-5d0332d5"]/div
    '''
if __name__ == '__main__':
    main()