import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Setup Options
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.maximize_window()

list_jobs = []

page = 1

while True:

    if page == 1:
        url = "https://www.naukrigulf.com/data-analyst-jobs-in-egypt"
    else:
        url = f"https://www.naukrigulf.com/data-analyst-jobs-in-egypt-{page}"

    print(f"Scraping Page {page}")
    
    driver.get(url)
    time.sleep(4)

    jobs = driver.find_elements(By.CLASS_NAME, 'srp-tuple')

    # stop if no jobs found (last page reached)
    if len(jobs) == 0:
        print("No more pages found")
        break

    for job in jobs:
        try:
            job_title = job.find_element(By.CLASS_NAME, 'designation-title').text
            job_link = job.find_element(By.CLASS_NAME, 'info-position').get_attribute('href')
            company_name = job.find_element(By.CLASS_NAME, 'info-org').text
            location = job.find_element(By.CLASS_NAME, 'info-loc').text
            post_date = job.find_element(By.CLASS_NAME, 'time').text

            list_jobs.append({
                'job_name': job_title,
                'company': company_name,
                'location': location,
                'date': post_date,
                'link': job_link,
                'source': 'Naukrigulf'
            })

        except:
            continue

    page += 1


df = pd.DataFrame(list_jobs)
print(df)

file_path = os.path.abspath("naukrigulf_jobs.xlsx")
df.to_excel(file_path, index=False)

print("Excel file saved successfully:", file_path)

driver.quit()