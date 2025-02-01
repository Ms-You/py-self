from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
import time

# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)

options = webdriver.ChromeOptions()
options.add_argument("window-size=1000,1000")
options.add_argument("no-sandbox")

browser = webdriver.Chrome(options=options)
browser.get("https://shopping.naver.com")

wait = WebDriverWait(browser, 10)

def find(wait, css_selector):
    return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

shopping_home_search_button = find(wait, "button._shoppingHomeSearch_button_gXyNO")
browser.execute_script("arguments[0].click();", shopping_home_search_button)
# shopping_home_search_button.send_keys(Keys.ENTER)

search = find(wait, "input[name=query]")
search.send_keys("아이폰 케이스\n")

time.sleep(5)

browser.close()