

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from utils.report_generator import save_test_result
import time

def test_currency_filter():
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")  
    
    # Initialize WebDriver with the proper service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    test_results = []
    base_url = "https://www.alojamiento.io/property/villa-sitges-colibri-with-mountain-view-pool-wi-fi-garden-terrace/HA-6515491183"
    page_url = base_url

    try:
        # Navigate to the test URL
        driver.get(base_url)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "js-price-value"))
        )
        
        try:
            currency_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "js-currency-sort-footer"))
            )
        except TimeoutException:
            currency_dropdown = driver.find_element(By.CSS_SELECTOR, "#js-currency-sort-footer")
        
        driver.execute_script("arguments[0].scrollIntoView(true);", currency_dropdown)
        time.sleep(2)  
        
        
        try:
            driver.execute_script("arguments[0].click();", currency_dropdown)
        except Exception:
            ActionChains(driver).move_to_element(currency_dropdown).click().perform()
        
        time.sleep(2)  
        currency_options = driver.find_elements(By.CSS_SELECTOR, "#js-currency-sort-footer .select-ul li")
        
        # Iterate through currency options
        for currency_option in currency_options:
            try:
                
                currency_code = currency_option.get_attribute("data-currency-country") or "Unknown"
                currency_symbol = currency_option.find_element(By.TAG_NAME, "p").text.strip()              
                
                driver.execute_script("arguments[0].click();", currency_option)
                
                WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element(
                        (By.CLASS_NAME, "js-price-value"), currency_symbol
                    )
                )
                
                property_tiles = driver.find_elements(By.CLASS_NAME, "js-price-value")
                
                updated_prices = [tile.text for tile in property_tiles]
                
                test_passed = all(currency_symbol in price for price in updated_prices)
                
                test_results.append({
                    'page_url': page_url,
                    'testcase': f"Currency Change to {currency_code}",
                    'passed': test_passed,
                    'comments': f"Updated prices: {updated_prices}"
                })
                
                driver.execute_script("arguments[0].click();", currency_dropdown)
                time.sleep(1)
                
            except Exception as e:
                print(f"Error processing currency {currency_code}: {str(e)}")
                test_results.append({
                    'page_url': page_url,
                    'testcase': f"Currency Change to {currency_code}",
                    'passed': False,
                    'comments': f"Test failed: {str(e)}"
                })
        
    except Exception as e:
        print(f"Critical error during test: {str(e)}")
        test_results.append({
            'page_url': page_url,
            'testcase': "Currency Change Test",
            'passed': False,
            'comments': f"Critical error: {str(e)}"
        })
    finally:
        save_test_result(test_results, sheet_name="Currency Filter Test")
        driver.quit()
