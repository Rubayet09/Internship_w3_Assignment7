# Internship_w3_Assignment7


## Vacation Rental Testing Automation

## Table of Contents 
1. [Overview](#overview) 
2. [Key Features](#key-features) 
3.  [Technologies Used](#technologies-used) 
5. [Development Setup](#development-setup) 
6. [Project Structure](#project-structure) 
7. [Author](#author)


## Overview
This project automates the testing of a vacation rental details page to validate essential elements and functionality. The automation script uses Python with the Selenium and Pandas libraries to perform the testing on the specific URL.

--- 
## Key Features 
- **H1 Tag Existence**: Checks if the H1 tag is present on the page.
- **HTML Tag Sequence**: Verifies the sequence of H1-H6 tags.
 - **Image Alt Attribute**: Ensures that all images have a valid alt attribute.
- **URL Status Code**: Checks the status code of all URLs on the page.
 - **Currency Filtering**: Validates the property tiles' currency changes according to the currency filter.
 - **Script Data Scraping**: Extracts and records the following data to an Excel file: [ Site URL, Campaign ID, Site Name, Browser, Country Code, IP Address ]
---

## Technologies Used

-   **Python**
-   **Selenium**
-   **Pandas**
-   **Google Chrome with WebDriver**


## Development Setup

### Prerequisites

Ensure the following are installed on your system:

- Python 3.6 or higher
- Google Chrome web browser
- Chromedriver
- Selenium Python library
- Pandas library
---

### Steps: 1. Clone the repository:
 ```bash 
git clone https://github.com/Rubayet09/Internship_w3_Assignment7.git 
cd Internship_w3_Assignment7
 ```

### Steps: 2. Create venv and install dependencies:
 ```bash 
python3 -m venv venv 
source venv/bin/activate

pip install -r requirements.txt

 ```

### Steps: 3. Run the test:
 ```bash 
python main.py
 ```

NB: After completing the test, a xlsx file will be created and the terminal will show you the text: 
** "Tests completed. Check the 'reports/test_results.xlsx' for results."**
 
### Steps: 4. Results:
Navigate to reports/test_results.xlsx where all the test reports have been generated.

--- 

## File Structure
```
vacation_rental_testing/
├── reports/
└── tests/
    ├── test_currency_filter.py
    ├── test_h1_existence.py
    ├── test_html_sequence.py
    ├── test_img.py
    ├── test_scripts.py
    └── test_url.py
├── utils/
    └── report_generator.py
└── main.py
```



## Author
Rubayet Shareen

Software Engineer Intern, 
W3 Engineers Ltd.
