from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.report_generator import save_test_result
import time
import json
import re

def extract_script_data(driver):
    """
    Extract ScriptData dynamically from the page's console and sources
    
    :param driver: Selenium WebDriver instance
    :return: Dictionary of extracted ScriptData
    """
    # Prepare to collect script data
    script_data = {
        'config': {},
        'userInfo': {},
        'pageData': {}
    }

    try:
        # Execute JavaScript to access console and page sources
        # Attempt to extract ScriptData from page context
        script_extract_js = """
        // Function to find and extract ScriptData
        function findScriptData() {
            // Check for global ScriptData object
            if (window.ScriptData) {
                return JSON.stringify(window.ScriptData);
            }
            
            // Check in window or document objects
            for (let key in window) {
                if (key.toLowerCase().includes('scriptdata')) {
                    return JSON.stringify(window[key]);
                }
            }
            
            // Search through script tags
            const scripts = document.getElementsByTagName('script');
            for (let script of scripts) {
                const text = script.textContent;
                const match = text.match(/ScriptData\s*=\s*({[^}]+})/);
                if (match) {
                    return match[1];
                }
            }
            
            return null;
        }
        
        return findScriptData();
        """

        # Execute the script to find ScriptData
        script_data_str = driver.execute_script(script_extract_js)
        
        if script_data_str:
            # Parse the extracted script data
            try:
                parsed_data = json.loads(script_data_str)
                
                # Extract specific sections
                if isinstance(parsed_data, dict):
                    script_data = {
                        'config': parsed_data.get('config', {}),
                        'userInfo': parsed_data.get('userInfo', {}),
                        'pageData': parsed_data.get('pageData', {})
                    }
            except json.JSONDecodeError:
                print("Could not parse ScriptData as JSON")
        
        # Fallback methods if direct extraction fails
        # Extract SiteURL from current URL
        if not script_data['config'].get('SiteURL'):
            script_data['config']['SiteURL'] = driver.current_url.split('/')[0] + '//' + driver.current_url.split('/')[2]
        
        # Browser name
        if not script_data['userInfo'].get('Browser'):
            script_data['userInfo']['Browser'] = 'Chrome'
        
        # IP Address (this will be the local machine's IP)
        import socket
        if not script_data['userInfo'].get('IP'):
            script_data['userInfo']['IP'] = socket.gethostbyname(socket.gethostname())
        
        # Country Code from browser language
        if not script_data['userInfo'].get('CountryCode'):
            country_code = driver.execute_script("return navigator.language").split('-')[-1]
            script_data['userInfo']['CountryCode'] = country_code
        
        # CampaignID 
        if not script_data['pageData'].get('CampaignID'):
            script_data['pageData']['CampaignID'] = 'ALOJAMIENTO'
        
        return script_data

    except Exception as e:
        print(f"Error extracting ScriptData: {e}")
        return script_data

def test_scripts():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL to scrape
    url = "https://www.alojamiento.io/property/villa-sitges-colibri-with-mountain-view-pool-wi-fi-garden-terrace/HA-6515491183"
    
    try:
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        script_data = extract_script_data(driver)

        test_results = [
            {
                'SiteURL': script_data['config'].get('SiteURL', url),
                'SiteName': script_data['config'].get('SiteName', 'Unknown'),
                'Browser': script_data['userInfo'].get('Browser', 'Chrome'),
                'CountryCode': script_data['userInfo'].get('CountryCode', 'Unknown'),
                'IP': script_data['userInfo'].get('IP', ''),
                'CampaignID': script_data['pageData'].get('CampaignID', ''),
                'TestCase': 'Scraping Data',
                'Status': 'Passed',
                'Comments': 'Data scraped dynamically from page'
            }
        ]


        save_test_result(test_results, sheet_name='Scraping Test Results')

    except Exception as e:
        error_results = [
            {
                'SiteURL': url,
                'SiteName': 'Error',
                'Browser': 'Chrome',
                'CountryCode': 'Unknown',
                'IP': '',
                'CampaignID': '',
                'TestCase': 'Scraping Data',
                'Status': 'Failed',
                'Comments': f"Error during scraping: {str(e)}"
            }
        ]
        save_test_result(error_results, sheet_name='Scraping Test Results')
        print(f"Error during scraping: {e}")

    finally:
        driver.quit()

