import sys
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from utils.report_generator import save_test_result

def test_html_sequence():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  
    chrome_options.binary_location = "/usr/bin/google-chrome"  

    service = Service(ChromeDriverManager().install())

    urls_to_test = [
        "https://www.alojamiento.io/property/villa-sitges-colibri-with-mountain-view-pool-wi-fi-garden-terrace/HA-6515491183"
    ]

    all_test_results = []

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        for url in urls_to_test:
            driver.get(url)
            
            header_tags = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")
            
            result = {
                "page_url": url,
                "testcase": "HTML Tag Sequence",
                "passed": False,
                "comments": ""
            }
            
            if not header_tags:
                result["comments"] = "No header tags found on the page."
                all_test_results.append(result)
                continue
            
            tag_names = [tag.tag_name for tag in header_tags]
            
            def validate_header_sequence(tags):
                tag_levels = [int(tag[1]) for tag in tags]
                
                for i in range(1, len(tag_levels)):
                    if tag_levels[i] > tag_levels[i-1] + 1:
                        return False
                return True
            
            if validate_header_sequence(tag_names):
                non_empty_headers = [tag for tag in header_tags if tag.text.strip()]
                
                if non_empty_headers:
                    result["passed"] = True
                    result["comments"] = f"Valid header sequence. Found {len(non_empty_headers)} non-empty headers."
                    
                    for i, tag in enumerate(non_empty_headers, 1):
                        result[f"Header_{i}_Type"] = tag.tag_name
                        result[f"Header_{i}_Text"] = tag.text.strip()
                else:
                    result["comments"] = "Header tags found but all are empty."
            else:
                result["comments"] = f"Invalid header sequence. Tags found: {tag_names}"
            
            all_test_results.append(result)
    
    except Exception as e:
        error_result = {
            "page_url": url,
            "testcase": "HTML Tag Sequence",
            "passed": False,
            "comments": f"Test execution error: {str(e)}"
        }
        all_test_results.append(error_result)
    
    finally:
        driver.quit()
        
        if all_test_results:
            save_test_result(all_test_results, sheet_name="HTML Tag Sequence")