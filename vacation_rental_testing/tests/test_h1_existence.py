import sys
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from utils.report_generator import save_test_result

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_h1_existence():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  
    chrome_options.binary_location = "/usr/bin/google-chrome"  

    service = Service(ChromeDriverManager().install())

    url_to_test = "https://www.alojamiento.io/property/villa-sitges-colibri-with-mountain-view-pool-wi-fi-garden-terrace/HA-6515491183"

    all_test_results = []
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url_to_test)
        
        h1_tags = driver.find_elements(By.TAG_NAME, "h1")
        
        for i, h1 in enumerate(h1_tags, 1):
            result = {
                "page_url": url_to_test,
                "testcase": f"H1 Tag Existence - H1 #{i}",
                "passed": False,
                "comments": ""
            }
            
            if h1.text.strip():
                result["passed"] = True
                result["comments"] = f"Valid H1 tag(s) found: {h1.text.strip()}"
            else:
                result["comments"] = f"Empty H1 tag found at index {i}."
            
            all_test_results.append(result)
       
    except Exception as e:
        error_result = {
            "page_url": url_to_test,
            "testcase": "H1 Tag Existence",
            "passed": False,
            "comments": f"Test execution error: {str(e)}"
        }
        all_test_results.append(error_result)
    
    finally:
        driver.quit()
        
        if all_test_results:
            save_test_result(all_test_results, sheet_name="H1 Tag Existence")