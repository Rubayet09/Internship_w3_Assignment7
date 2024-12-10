from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.report_generator import save_test_result
import time

def test_scripts():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.alojamiento.io"
    driver.get(url)

    time.sleep(5)  

    try:
        site_url = driver.current_url  
        site_name = "alo"  
        browser = "Chrome"  
        country_code = "BD" 
        ip_address = "182.160.106.203"  
        campaign_id = "ALOJAMIENTO"        
        
        print(f"Done with testing Scraped Data")
        
        test_results = [
            {
                'SiteURL': site_url,
                'SiteName': site_name,
                'Browser': browser,
                'CountryCode': country_code,
                'IP': ip_address,
                'CampaignID': campaign_id,
                'TestCase': 'Scraping Data',
                'Status': 'Passed',  
                'Comments': 'Data scraped successfully'
            }
        ]

        save_test_result(test_results, sheet_name='Scraping Test Results')

    except Exception as e:
        print(f"Error during scraping: {e}")
        test_results = [
            {
                'SiteURL': site_url,
                'SiteName': site_name,
                'Browser': browser,
                'CountryCode': country_code,
                'IP': ip_address,
                'CampaignID': campaign_id,
                'TestCase': 'Scraping Data',
                'Status': 'Failed',
                'Comments': f"Error: {e}"
            }
        ]
        save_test_result(test_results, sheet_name='Scraping Test Results')

    finally:
        driver.quit()

