from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
import pyperclip
from dotenv import load_dotenv # 환경변수를 불러오기 위함
import json

load_dotenv()

options = webdriver.ChromeOptions()
options.add_argument("window-size=1000,1000")

browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)
short_wait = WebDriverWait(browser, 3)

browser.get("https://shopping.naver.com")

def presence_find(wait, css_selector):
    return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

def visibility_find(wait, css_selector):
    return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))

# 로그인 버튼 클릭
login_button = visibility_find(wait, "button.loginMobile_button__jPFRe")
login_button.click()

input_id = visibility_find(wait, "input#id")
input_pw = visibility_find(wait, "input#pw")

# 로그인
pyperclip.copy(os.getenv("login_id"))
input_id.send_keys(Keys.CONTROL, "v")
pyperclip.copy(os.getenv("login_password"))
input_pw.send_keys(Keys.CONTROL, "v")
input_pw.send_keys("\n")

# 로그인 여부 확인
presence_find(wait, "a#gnb_logout_button")

# 검색창 클릭
shopping_home_search_button = presence_find(wait, "button._shoppingHomeSearch_button_gXyNO")
browser.execute_script("arguments[0].click();", shopping_home_search_button)

# 검색
search = visibility_find(wait, "input[name=query]")
search.send_keys("아이폰 케이스")
time.sleep(0.5)
search.send_keys("\n")

# 상품 목록을 찾을 때까지 대기
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class^=basicProductCard_basic_product_card__TdrHT]")))  # div로 변경
time.sleep(1)

# # 스크롤
# for i in range(8):
#     browser.execute_script("window.scrollBy(0, " + str((i+1) * 1000) + ")")
#     time.sleep(1)

product_list = browser.find_elements(By.CSS_SELECTOR, "div[class^=basicProductCard_basic_product_card__TdrHT]")

# for product in product_list:
#     # 광고 제외
#     advertisement_buttons = product.find_elements(By.CSS_SELECTOR, "div[class^=basicProductCardInformation_advertisement_area__HzaQ_]")
#     if advertisement_buttons:  # 광고 요소가 존재하면
#         continue

#     # 상품명 추출
#     title_element = product.find_element(By.CSS_SELECTOR, "strong[class^=basicProductCardInformation_title__Bc_Ng]")
#     product_name = title_element.text
#     print(f"상품명: {product_name}")


# 첫 번째 상품 클릭
if product_list:
    first_product_link = product_list[0].find_element(By.CSS_SELECTOR, "a.basicProductCard_link__urzND")
    first_product_link.click()
else:
    print("상품 목록이 비어 있습니다.")

# 새탭으로 이동
browser.switch_to.window(browser.window_handles[1])

# 상품 옵션 선택
visibility_find(wait, "a[aria-haspopup='listbox']")
options = browser.find_elements(By.CSS_SELECTOR, "a[aria-haspopup='listbox']")

# 첫 번째 옵션에서 두 번째 항목 선택
options[0].click()
time.sleep(0.5)
browser.find_element(By.CSS_SELECTOR, "ul[role=listbox] li:nth-child(2) a[role=option]").click()

# 두 번째 옵션에서 첫 번째 항목 선택
options[1].click()
time.sleep(0.5)
browser.find_element(By.CSS_SELECTOR, "ul[role=listbox] li:first-child a[role=option]").click()

# 구매하기 버튼 클릭
buy_button = browser.find_element(By.CSS_SELECTOR, "div.sys_chk_buy a")
buy_button.click()

time.sleep(3)

browser.close()