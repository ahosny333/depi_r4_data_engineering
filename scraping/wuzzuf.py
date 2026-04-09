from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
#for excel saved in excel sheet
import os
import pandas as pd

#import mysql.connector

#input_text = input("Enter the job title: ")
input_text = 'Data Analyst'
url = "https://wuzzuf.net/jobs/egypt"
 
list_jobs = []
 
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
 
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(url)
 
driver.find_element(By.NAME, 'q').send_keys(input_text)
 
driver.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div[2]/div[1]/form/button').click()
 
time.sleep(5)
jobs = driver.find_elements(By.CLASS_NAME, 'css-pkv5jc')
 
for job in jobs:
     job_title = job.find_element(By.CLASS_NAME, 'css-o171kl').text
     company_name = job.find_element(By.CLASS_NAME, 'css-ipsyv7').text
     location = job.find_element(By.CLASS_NAME, 'css-16x61xq').text
     tags = job.find_element(By.CLASS_NAME, 'css-5jhz9n').text
     link_element = job.find_element(By.CSS_SELECTOR, 'a.css-o171kl')
     relative_link = link_element.get_attribute('href')
 
     list_jobs.append({
        'job_name': job_title,
        'company': company_name,
        'location': location,
        'tags': tags,
        'link': relative_link

    })
     


df = pd.DataFrame(list_jobs)
print(df)
# file_path = os.path.abspath("wuzzuf_jobs5.xlsx")
# df.to_excel(file_path, index=False)
# print("Excel file saved successfully:", file_path)



# connect to mysql
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="123456",   # empty in XAMPP default
#     database="wuzzuf_jobs"
# )

# cursor = conn.cursor()

# # insert data
# for job in list_jobs:
#     query = """
#     INSERT INTO jobs (job_name, company, location, tags)
#     VALUES (%s, %s, %s, %s)
#     """
#     values = (
#         job['job_name'],
#         job['company'],
#         job['location'],
#         job['tags']
#     )
#     cursor.execute(query, values)  # ✅ inside loop
# conn.commit()
# cursor.close()
# conn.close()
# print("Data inserted successfully")

driver.quit()