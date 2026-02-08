import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# ---------- Project Root Path ----------
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
download_path = os.path.join(project_root, "data", "raw_json")
os.makedirs(download_path, exist_ok=True)

print("Download folder:", download_path)

# ---------- Required ZIP Files ----------
required_files = [
    "tests_json.zip",
    "odis_json.zip",
    "t20s_json.zip",
    "ipl_json.zip"
]

# ---------- Selenium Setup ----------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://cricsheet.org/downloads/"
driver.get(url)

time.sleep(5)

links = driver.find_elements(By.TAG_NAME, "a")

download_links = []

for link in links:
    href = link.get_attribute("href")
    if href:
        for file in required_files:
            if href.endswith(file):
                download_links.append(href)

print(f"\nRequired ZIP files found: {len(download_links)}\n")

# ---------- Download ----------
for link in download_links:
    filename = link.split("/")[-1]
    filepath = os.path.join(download_path, filename)

    if os.path.exists(filepath):
        print(f"{filename} already exists — skipping")
        continue

    print(f"Downloading {filename}...")

    r = requests.get(link)
    with open(filepath, "wb") as f:
        f.write(r.content)

print("\nAll required downloads completed ✅")

driver.quit()
