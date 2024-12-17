#Scraping Forbes 400 List
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.forbes.com/forbes-400/')
print(driver.page_source)
driver.quit()