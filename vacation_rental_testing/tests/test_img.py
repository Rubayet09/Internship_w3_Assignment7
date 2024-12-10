
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.report_generator import save_test_result

def test_img():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    test_results = []

    try:
        driver.get("https://www.alojamiento.io/property/villa-sitges-colibri-with-mountain-view-pool-wi-fi-garden-terrace/HA-6515491183")

        images = driver.find_elements("tag name", "img")

        if not images:
            test_results.append({
                "page_url": driver.current_url,
                "testcase": "Image Alt Attribute",
                "passed": False,
                "comments": "No images found on the page.",
                "image_src": "N/A"  
            })
        else:
            for i, img in enumerate(images):
                alt_text = img.get_attribute("alt")
                img_src = img.get_attribute("src")  
                result = {
                    "page_url": driver.current_url,
                    "testcase": f"Image Alt Attribute - Image #{i+1}",
                    "passed": bool(alt_text and alt_text.strip()),
                    "comments": f"Alt attribute {'is present' if alt_text else 'is missing'}.",
                    "image_src": img_src  
                }
                test_results.append(result)

    except Exception as e:
        test_results.append({
            "page_url": driver.current_url,
            "testcase": "Image Alt Attribute",
            "passed": False,
            "comments": f"Error: {str(e)}",
            "image_src": "N/A"  
        })
    finally:
        save_test_result(test_results, sheet_name="Image Alt Attribute")
        driver.quit()

