from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://cricsheet.org/matches/"
driver.get(url)

time.sleep(5)

# Extract all page links
links = driver.find_elements(By.TAG_NAME, "a")

format_links = []

for link in links:
    href = link.get_attribute("href")
    if href and any(x in href for x in ["odis", "t20s", "tests", "ipl"]):
        format_links.append(href)

print("Match format pages found:\n")

for l in format_links:
    print(l)

driver.quit()