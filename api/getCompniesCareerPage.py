# Name: Dong Han
# Mail: dongh@mun.ca
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import random
import api.database_handle
import psycopg2

class BaseScraper:
    def __init__(self,company,url):
        self.company = company
        self.url = url
        self.driver = self._initialize_driver()
        self.db, self.cursor = api.database_handle.connectDB()

    def _initialize_driver(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
        options.add_argument("--headless")

        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def simulate_human_operation(self):
        # Random delay
        time.sleep(random.uniform(1, 3))
        # Simulate human-like mouse movements
        action = ActionChains(self.driver)
        action.move_to_element(self.driver.find_element(By.TAG_NAME, 'body')).perform()
        action.move_by_offset(random.randint(10, 100), random.randint(10, 100)).perform()

        # Wait for the page to load completely
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda d: d.execute_script("return document.readyState === 'complete';"))

    def scrape(self,*arg):
        job_file_id = self.company + "_" + datetime.now().strftime("%Y-%m-%d")
        # connect MySQL check if record existed

        api.database_handle.createTable(self.cursor)

        json_data = is_job_json_existed_in_mysql(job_file_id, self.cursor)

        if json_data:
            return json_data
        return self.indivisual_scrape(job_file_id)

    def indivisual_scrape(self,*args):
        pass

    def close_driver(self):
        self.driver.quit()

class VerafinScraper(BaseScraper):
    def indivisual_scrape(self,job_file_id):
        self.driver.get(self.url)
        self.simulate_human_operation()
        all_items = {}
        try:
            # get the <li> quantities within <ul>
            list_item_count = len(self.driver.find_elements(By.XPATH, "//*[@id='mainContent']/div/div[2]/section/ul/li"))
            # print(list_item_count)

            for i in range(1, list_item_count + 1):
                item = self.driver.find_element(By.XPATH, f"//*[@id='mainContent']/div/div[2]/section/ul/li[{i}]")

                jobID = item.find_element(By.CSS_SELECTOR, "ul[data-automation-id='subtitle'] > li").text
                jobItemPart = item.find_element(By.CSS_SELECTOR, "h3 > a")
                all_items[jobID] = {
                    "job_title": jobItemPart.text,
                    "link": jobItemPart.get_attribute("href")
                }
            json_string = json.dumps(all_items)
            api.database_handle.saveJsonFileToTable(job_file_id, json_string, self.db, self.cursor)
            self.db.commit()
            self.db.close()
            return all_items

        except TimeoutException:
            print("Timed out waiting for page to load")
            self.driver.save_screenshot('debug_screenshot_after_timeout.png')
            return
        except NoSuchElementException:
            print("Could not find the elements within it.")
            return "1"

class ColabScraper(BaseScraper):
    def indivisual_scrape(self,job_file_id):
        self.driver.get(self.url)
        self.simulate_human_operation()
        all_items = {}
        try:
            # get the .career-grid-list  have <a>
            list_item_count = len( self.driver.find_elements(By.XPATH, "//div[contains(@class, 'career-grid-list')]/a"))

            for i in range(1, list_item_count + 1):
                item =  self.driver.find_element(By.XPATH, f"//div[contains(@class, 'career-grid-list')]/a[{i}]")
                jobLink = item.get_attribute("href")
                job_title = item.find_element(By.CSS_SELECTOR, "h6").text
                jobID = jobLink.split("/")[-1]
                all_items[jobID] = {
                    "job_title": job_title,
                    "link": jobLink
                }

            json_string = json.dumps(all_items)
            api.database_handle.saveJsonFileToTable(job_file_id, json_string, self.db, self.cursor)
            self.db.commit()
            self.db.close()
            return all_items

        except TimeoutException:
            print("Timed out waiting for page to load")
            self.driver.save_screenshot('debug_screenshot_after_timeout.png')
            return
        except NoSuchElementException:
            print("Could not find the elements within it.")
            return "1"

class Vission33Scraper(BaseScraper):
    def indivisual_scrape(self,job_file_id):
        self.driver.get(self.url)
        self.simulate_human_operation()
        all_items = {}
        try:
            job_posts = self.driver.find_elements(By.XPATH,
                                             '//*[@id="root"]/div/div/div/div/div/div/div[3]/div/div/div/div/div/div[2]/div[2]/div/a')

            # Extract data and populate a dictionary
            for jobItem in job_posts:
                job_title = jobItem.find_element(By.XPATH, ".//div[contains(@class, 'col-md-3')][1]").text

                link = jobItem.get_attribute("href")
                jobID = link.split("/")[-1].split("-")[
                    0]  # get 16347046 from jobs.vision33.com/careers/31076-Vision33/jobs/16347046-ByDesign-Implementation-Consultant

                all_items[jobID] = {
                    'job_title': job_title,
                    'link': link
                }
            json_string = json.dumps(all_items)
            api.database_handle.saveJsonFileToTable(job_file_id, json_string, self.db, self.cursor)
            self.db.commit()
            self.db.close()
            return all_items

        except TimeoutException:
            print("Timed out waiting for page to load")
            self.driver.save_screenshot('debug_screenshot_after_timeout.png')
            return
        except NoSuchElementException:
            print("Could not find the elements within it.")
            return "1"

class MysaScraper(BaseScraper):
    def indivisual_scrape(self,job_file_id):
        self.driver.get(self.url)
        self.simulate_human_operation()
        all_items = {}
        try:
            container_xpath = "//*[@id='lever-jobs-container']"
            # Find all <a> elements within the container
            a_elements = self.driver.find_elements(By.XPATH, f"{container_xpath}//a")
            for a in a_elements:
                job_title = a.text
                jobLink = a.get_attribute('href')
                jobID = jobLink.split("/")[-1]
                all_items[jobID] = {
                    "job_title": job_title,
                    "link": jobLink
                }

            json_string = json.dumps(all_items)
            api.database_handle.saveJsonFileToTable(job_file_id, json_string, self.db, self.cursor)
            self.db.commit()
            self.db.close()
            return all_items

        except TimeoutException:
            print("Timed out waiting for page to load")
            self.driver.save_screenshot('debug_screenshot_after_timeout.png')
            return
        except NoSuchElementException:
            print("Could not find the elements within it.")
            return "1"

class AvalonHolographics(BaseScraper):
    def indivisual_scrape(self,job_file_id):
        self.driver.get(self.url)
        self.simulate_human_operation()
        all_items = {}
        try:
            section_items = self.driver.find_element(By.TAG_NAME, "section")
            h2_elements = section_items.find_elements(By.TAG_NAME, "h2")
            for i in range(1, len(h2_elements)):
                job_title = h2_elements[i].text
                jobID = job_file_id + "_" + str(i)
                all_items[jobID] = {
                    'job_title': job_title,
                    'link': self.url  # it doesnt have indivial link
                }
            json_string = json.dumps(all_items)
            api.database_handle.saveJsonFileToTable(job_file_id, json_string, self.db, self.cursor)
            self.db.commit()
            self.db.close()
            self.close_driver()
            return all_items

        except TimeoutException:
            print("Timed out waiting for page to load")
            self.driver.save_screenshot('debug_screenshot_after_timeout.png')
            return
        except NoSuchElementException:
            print("Could not find the elements within it.")
            return "1"

class PolyUnitScraper(BaseScraper):
    def scrape(self,*args):
        return "1" # No job post It's manual check and Need to check later in case any job posted

class EnaimcoScraper(BaseScraper):
    def scrape(self,*args):
        return "1" # No job post It's manual check and Need to check later in case any job posted

class StrobelScraper(BaseScraper):
    def scrape(self,*args):
        return "2" # wait for building

class OtherOceanScraper(BaseScraper):
    def scrape(self,*args):
        return "2" # wait for building

class SiftMedScraper(BaseScraper):
    def scrape(self,*args):
        return "3" # No Careers on its Official wensite

class ScraperFactory:
    @staticmethod
    def get_scraper(company, url):
        scrapers = {
            "verafin": VerafinScraper,
            "colab": ColabScraper,
            "polyunit": PolyUnitScraper,
            "vision33": Vission33Scraper,
            "mysa": MysaScraper,
            "strobel tek": StrobelScraper,
            "other ocean": OtherOceanScraper,
            "avalon": AvalonHolographics,
            "enaimco": EnaimcoScraper,
            "siftmed": SiftMedScraper
        }
        scraper = scrapers.get(company.lower())
        if scraper:
            return scraper(company,url)
        return None

def is_job_json_existed_in_mysql(job_file_id,cursor,tableName="nl_tech_jobs"):
    try:
        sql = f"select json_data from {tableName} where job_id = %s"
        cursor.execute(sql,(job_file_id,))

        result = cursor.fetchone()

        if result and result[0]: # also check the json_data is not empty
            json_data = json.loads(result[0])
            return json_data
        else:
            return None
    except psycopg2.Error as err:
        print(f"Error in is_job_json_existed_in_mysql: {err}")
        return None

#################################################### main for testing ###################################
# def main():
#     # mysaurl = "https://getmysa.com/pages/careers-ca"
#     # company = "mysa"
#     # scraper = ScraperFactory.get_scraper(company,mysaurl)
#     # print(scraper.scrape())
#
#     verafin_link = "https://nasdaq.wd1.myworkdayjobs.com/en-US/US_External_Career_Site?q=verafin"
#     company = "verafin"
#     scraper = ScraperFactory.get_scraper(company, verafin_link)
#     print(scraper.scrape())
#
#     # colab_link = "https://www.colabsoftware.com/careers#openings"
#     # jobfile = checkColab(colab_link)
#     # print(jobfile)
#
#     # polu_link = "https://www.polyunity.com/work-with-us"
#     #
#     # vission33_link = "https://jobs.vision33.com/"
#     # s = checkVission33(vission33_link)
#
#     # avalonholo = "https://www.avalonholographics.com/careers"
#     # s = checkAvalonholo(avalonholo)
#     # print(s)
#
#     '''
#     //*[@id="postings"]/div
#
#     '''
# if __name__ == '__main__':
#     main()
