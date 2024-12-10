import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.report_generator import save_test_result

def test_url():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    test_results = []

    try:
        driver.get("https://www.alojamiento.io/property/villa-sitges-colibri-with-mountain-view-pool-wi-fi-garden-terrace/HA-6515491183")
        
        links = driver.find_elements("tag name", "a")

        if not links:
            test_results.append({
                "page_url": driver.current_url,
                "testcase": "URL Status Code Check",
                "passed": False,
                "comments": "No links found on the page.",
                "URLs": "N/A"  
            })
        else:
            for i, link in enumerate(links):
                url = link.get_attribute("href")
                
                if url:  # Make sure the link has an href attribute
                    try:
                        response = requests.get(url)
                        
                        # If the status code is 404, report failure
                        if response.status_code == 404:
                            result = {
                                "page_url": driver.current_url,
                                "testcase": f"URL Status Code Check - Link #{i+1}",
                                "passed": False,
                                "comments": f"404 error: Page not found",
                                "URLs": url  # Add the URL being tested
                            }
                        else:
                            result = {
                                "page_url": driver.current_url,
                                "testcase": f"URL Status Code Check - Link #{i+1}",
                                "passed": True,
                                "comments": f"Status code {response.status_code}.",
                                "URLs": url  
                            }
                    except requests.exceptions.RequestException as e:
                        result = {
                            "page_url": driver.current_url,
                            "testcase": f"URL Status Code Check - Link #{i+1}",
                            "passed": False,
                            "comments": f"Broken URL or connection error",
                            "URLs": url 
                        }

                    test_results.append(result)
    
    except Exception as e:
        test_results.append({
            "page_url": driver.current_url,
            "testcase": "URL Status Code Check",
            "passed": False,
            "comments": f"Error: {str(e)}",
            "URLs": "N/A"  # No URLs tested in case of a general error
        })
    finally:
        save_test_result(test_results, sheet_name="URL Status Code Check")
        driver.quit()
