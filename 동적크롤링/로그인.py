from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
import pyperclip

options = webdriver.ChromeOptions()

browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)
short_wait = WebDriverWait(browser, 3)

browser.get("https://shopping.naver.com")

def find(wait, css_selector):
    return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))

login_button = find(wait, "button.loginMobile_button__jPFRe")
login_button.click()

input_id = find(wait, "input#id")
input_pw = find(wait, "input#pw")

pyperclip.copy("아이디")
input_id.send_keys(Keys.CONTROL, "v")
pyperclip.copy("비밀번호")
input_pw.send_keys(Keys.CONTROL, "v")
input_pw.send_keys("\n")

time.sleep(3)

browser.close()