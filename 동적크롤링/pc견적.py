from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()

browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)

def presence_element(css):
    return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))

def presence_elements(css):
    return wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css)))

def presence_element_browser(css):
    presence_element(css)
    return browser.find_element(By.CSS_SELECTOR, css)

def presence_elements_browser(css):
    presence_elements(css)
    return browser.find_elements(By.CSS_SELECTOR, css)

def visibility_element(css):
    return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))

def visibility_elements(css):
    return wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, css)))

def visibility_element_browser(css):
    visibility_element(css)
    return browser.find_element(By.CSS_SELECTOR, css)

def visibility_elements_browser(css):
    visibility_elements(css)
    return browser.find_elements(By.CSS_SELECTOR, css)

def choose_one(text, options):
    print("----------------------")
    print(text)
    print("----------------------")
    
    for i in range(len(options)):
        print(f"{i+1}. {options[i]}")
    choose = input("-> ")
    return int(choose) - 1

def parse_product():
    products = []
    for p in visibility_elements("table.tbl_list tbody tr[class^=productList_]"):
        try:
            name = p.find_element(By.CSS_SELECTOR, "p.subject a").text
            price = p.find_element(By.CSS_SELECTOR, "span.prod_price").text
        except:
            continue
        products.append((name, price))
    return products

category = {
    "cpu": "873",
    "메인보드": "875",
    "메모리": "874",
    "그래픽카드": "876",
    "ssd": "32617",
    "케이스": "879",
    "파워": "880",
}

category_css = {
    c: "dd.category_" + category[c] + " a" for c in category
}

browser.get("https://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=index&marketPlaceSeq=16&logger_kw=dnw_gnb_esti")

# cpu 카테고리 클릭
cpu_button = visibility_element(category_css["cpu"])
cpu_button.click()
time.sleep(0.5)

# CPU 제조사 가져오기
manufacturer_elements = visibility_elements_browser("div.search_option_item:nth-child(1) ul.search_cate_list li.search_cate_item span.item_text")
manufacturer_list = [element.text for element in manufacturer_elements]

# 제조사 목록이 비어있지 않은지 확인
if not manufacturer_list:
    print("제조사 목록을 가져오는 데 실패했습니다.")
else:
    chosen_index = choose_one("CPU 제조사를 골라주세요.", manufacturer_list)
    chosen_manufacturer = manufacturer_list[chosen_index]
    print(f"선택한 제조사: {chosen_manufacturer}")

    # 제조사 체크박스 클릭
    manufacturer_checkbox = visibility_element_browser(f"input[data='{chosen_manufacturer}']")
    browser.execute_script("arguments[0].click();", manufacturer_checkbox)


    # 제조사에 따른 cpu 종류 가져오기
    if chosen_manufacturer == "인텔":
        # 더보기 버튼
        more_button = visibility_element("div.search_option_item:nth-child(2) button.btn_item_more")
        browser.execute_script("arguments[0].click();", more_button)
        time.sleep(1)
        # cpu 종류
        manufacturers_cpu_elements = visibility_elements_browser("div.search_option_item:nth-child(2) ul.search_cate_list li.search_cate_item span.item_text")
    elif chosen_manufacturer == "AMD":
        more_button = visibility_element("div.search_option_item:nth-child(3) button.btn_item_more")
        browser.execute_script("arguments[0].click();", more_button)
        time.sleep(1)
        manufacturers_cpu_elements = visibility_elements_browser("div.search_option_item:nth-child(3) ul.search_cate_list li.search_cate_item span.item_text")

    # cpu 목록이 비어있는지 확인
    if not manufacturers_cpu_elements:
        print(f"{chosen_manufacturer}에 대한 CPU 목록을 가져오는 데 실패했습니다.")
    else:
        cpu_list = [element.text for element in manufacturers_cpu_elements]
        chosen_index = choose_one(f"{chosen_manufacturer} CPU 종류를 선택해주세요.", cpu_list)
        chosen_cpu = cpu_list[chosen_index] + " " # 뒤에 공백이 추가되어 있음
        print(f"선택한 CPU: {chosen_cpu}")

        # cpu 종류 체크박스 클릭
        cpu_checkbox = visibility_element_browser(f"input[data='{chosen_cpu}']")
        browser.execute_script("arguments[0].click();", cpu_checkbox)

        products = parse_product()
        for p in products:
            print(p)

time.sleep(3)

browser.close()