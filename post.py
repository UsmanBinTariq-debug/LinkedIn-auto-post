import os
import time
import uuid  # Add this import for generating unique directories
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Fetch credentials from environment variables
linkedin_username = os.getenv("LINKEDIN_USERNAME")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Generate a unique user data directory
unique_dir = f"/tmp/chrome-user-data-{uuid.uuid4()}"
chrome_options.add_argument(f"--user-data-dir={unique_dir}")

chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")  
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# Run Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print("Opening LinkedIn login page...")
    driver.get("https://www.linkedin.com/login")
    
    # Wait for username field
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

    print("Entering credentials...")
    driver.find_element(By.ID, "username").send_keys(linkedin_username)
    driver.find_element(By.ID, "password").send_keys(linkedin_password)

    # Click login button
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Wait for LinkedIn to process login (handle possible CAPTCHA delays)
    time.sleep(5)

    # Confirm login success
    WebDriverWait(driver, 15).until(EC.url_contains("feed"))
    print("Login successful!")

    # Navigate to post box
    driver.get("https://www.linkedin.com/feed/")
    post_box = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share-box__open')]"))
    )
    post_box.click()
    print("Opened post box.")

    # Write post
    text_area = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "ql-editor")))
    text_area.send_keys("Automated LinkedIn Post using Selenium!")
    print("Typed post content.")

    # Click Post
    post_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share-actions__primary-action')]"))
    )
    post_button.click()
    print("Post successful!")

finally:
    driver.quit()
