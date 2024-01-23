# Name: Dong Han
# Mail: dongh@mun.ca

import time
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

            jobItemPart = item.find_element(By.CSS_SELECTOR,"h3 > a")
            all_items[jobItemPart.text] = jobItemPart.get_attribute("href")

        return all_items

    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.save_screenshot('debug_screenshot_after_timeout.png')
        return
    except NoSuchElementException:
        print("Could not find the elements within it.")
        return
    finally:
        driver.quit()

def checkColab():
    pass

def main():
    verafin_link = "https://nasdaq.wd1.myworkdayjobs.com/en-US/US_External_Career_Site?q=verafin"
    jobs = checkVerafin(verafin_link)
    print(jobs)
    '''
    #mainContent > div > div.css-uvpbop > section > ul
    #mainContent > div > div.css-uvpbop > section > ul > li:nth-child(1)
    //*[@id="mainContent"]/div/div[2]/section/ul/li[1]
    #mainContent > div > div.css-uvpbop > section > ul > li:nth-child(2)
    #mainContent > div > div.css-uvpbop > section > ul > li:nth-child(8)
    
    //*[@id="mainContent"]/div/div[2]/section/ul/li[1]
    //*[@id="mainContent"]/div/div[2]/section/ul/li[2]
    //*[@id="mainContent"]/div/div[2]/section/ul/li[3]
    
    '''
if __name__ == '__main__':
    main()