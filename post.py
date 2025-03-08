import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Fetch credentials from GitHub Secrets
linkedin_username = os.getenv("LINKEDIN_USERNAME")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")  
chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")  # Unique user-data-dir

# Initialize WebDriver with options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.linkedin.com/login")

# Login
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
username.send_keys(linkedin_username)
password.send_keys(linkedin_password)
password.send_keys(Keys.RETURN)

# Wait for feed page to load
WebDriverWait(driver, 10).until(EC.url_contains("feed"))

# Navigate to post box
driver.get("https://www.linkedin.com/feed/")
post_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[strong[contains(text(), 'Start a post')]]"))
)
post_box.click()

# Write and post
text_area = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ql-editor")))
text_area.send_keys("Automated LinkedIn Post using Selenium!")

# Click Post
post_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "share-actions__primary-action"))
)
post_button.click()

# Close browser
driver.quit()
