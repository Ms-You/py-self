from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()

browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 10)

category = {
    "cpu": "873",
    "메인보드": "875",
    "메모리": "874",
    "그래픽카드": "876",
    "ssd": "32617",
    "케이스": "879",
    "파워": "880",
}

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

    for p in products:
        print(p)

    return products

category_css = {
    c: "dd.category_" + category[c] + " a" for c in category
}

def change_category(category_name):
    category_button = visibility_element(category_css[category_name])
    category_button.click()
    time.sleep(0.5)

# 체크박스 클릭
def click_checkbox(chosen_maker):
    maker_checkbox = visibility_element_browser(f"input[data='{chosen_maker}']")
    browser.execute_script("arguments[0].click();", maker_checkbox)

def choose_maker(text):
    # 제조사 더보기 버튼 있는 경우 클릭
    try:
        more_button = visibility_element("div.search_option_item:nth-child(1) button.btn_item_more")
        browser.execute_script("arguments[0].click();", more_button)
        time.sleep(1)
    except:
        pass

    maker_elements = visibility_elements_browser("div.search_option_item:nth-child(1) ul.search_cate_list li.search_cate_item span.item_text")
    maker_list = [element.text for element in maker_elements]

    # 제조사 목록이 비어있지 않은지 확인
    if not maker_list:
        print("제조사 목록을 가져오는 데 실패했습니다.")
    else:
        chosen_index = choose_one(text, maker_list)
        chosen_maker = maker_list[chosen_index]
        print(f"선택한 제조사: {chosen_maker}")

        # 선택한 제조사 체크박스 클릭
        click_checkbox(chosen_maker)
    return chosen_maker


browser.get("https://shop.danawa.com/virtualestimate/?controller=estimateMain&methods=index&marketPlaceSeq=16&logger_kw=dnw_gnb_esti")

########################## cpu ##########################
# cpu 카테고리 클릭
change_category("cpu")

# CPU 제조사 가져오기
chosen_maker = choose_maker("cpu 제조사를 골라주세요.")

# 제조사에 따른 cpu 종류 가져오기
if chosen_maker == "인텔":
    # 더보기 버튼
    more_button = visibility_element("div.search_option_item:nth-child(2) button.btn_item_more")
    browser.execute_script("arguments[0].click();", more_button)
    time.sleep(1)
    # cpu 종류
    manufacturers_cpu_elements = visibility_elements_browser("div.search_option_item:nth-child(2) ul.search_cate_list li.search_cate_item span.item_text")
elif chosen_maker == "AMD":
    more_button = visibility_element("div.search_option_item:nth-child(3) button.btn_item_more")
    browser.execute_script("arguments[0].click();", more_button)
    time.sleep(1)
    manufacturers_cpu_elements = visibility_elements_browser("div.search_option_item:nth-child(3) ul.search_cate_list li.search_cate_item span.item_text")

# cpu 목록이 비어있는지 확인
if not manufacturers_cpu_elements:
    print(f"{chosen_maker}에 대한 CPU 목록을 가져오는 데 실패했습니다.")
else:
    cpu_list = [element.text for element in manufacturers_cpu_elements]
    chosen_index = choose_one(f"{chosen_maker} CPU 종류를 선택해주세요.", cpu_list)
    chosen_cpu = cpu_list[chosen_index] + " " # 뒤에 공백이 추가되어 있음
    print(f"선택한 CPU: {chosen_cpu}")

    # cpu 종류 체크박스 클릭
    cpu_checkbox = visibility_element_browser(f"input[data='{chosen_cpu}']")
    browser.execute_script("arguments[0].click();", cpu_checkbox)

    # 조회된 cpu 목록 가져오기기
    products = parse_product()

########################## 메인보드 ##########################

# 메인보드 카테고리 클릭
change_category("메인보드")

# 메인보드 제조사 가져오기
chosen_maker = choose_maker("cpu 제조사를 골라주세요.")

# 제품 분류 가져오기
product_classify = visibility_elements_browser("div.search_option_item:nth-child(2) ul.search_cate_list li.search_cate_item span.item_text")
product_classify_list = [element.text for element in product_classify]

chosen_index = choose_one("제품 분류를 골라주세요.", product_classify_list)
chosen_product_classify = product_classify_list[chosen_index] + " " # 뒤에 공백이 있음
print(f"선택한 제조사: {chosen_product_classify}")

# 제품 분류 체크박스 클릭
click_checkbox(chosen_product_classify)

# 조회된 메인보드 목록 가져오기
products = parse_product()

########################## 메모리 ##########################

# 메모리 카테고리 클릭
change_category("메모리")

# 메모리 제조사 가져오기
chosen_maker = choose_maker("cpu 제조사를 골라주세요.")

# 사용 장치 가져오기
use_device = visibility_elements_browser("div.search_option_item:nth-child(2) ul.search_cate_list li.search_cate_item span.item_text")
use_device_list = [element.text for element in use_device]

chosen_index = choose_one("제품 분류를 골라주세요.", use_device_list)
chosen_use_device = use_device_list[chosen_index] + " " # 뒤에 공백이 있음
print(f"선택한 사용장치: {chosen_use_device}")

# 사용 장치 체크박스 클릭
click_checkbox(chosen_use_device)

# 제품 분류 가져오기
product_classify = visibility_elements_browser("div.search_option_item:nth-child(3) ul.search_cate_list li.search_cate_item span.item_text")
product_classify_list = [element.text for element in product_classify]

chosen_index = choose_one("제품 분류를 골라주세요.", product_classify_list)
chosen_product_classify = product_classify_list[chosen_index] + " " # 뒤에 공백이 있음
print(f"선택한 제품 분류: {chosen_product_classify}")

# 제품 분류 체크박스 클릭
click_checkbox(chosen_product_classify)

# 메모리 용량 더보기 버튼 클릭
more_button = visibility_element("div.search_option_item:nth-child(4) button.btn_item_more")
browser.execute_script("arguments[0].click();", more_button)
time.sleep(1)

# 메모리 용량 가져오기
memory_capacity = visibility_elements_browser("div.search_option_item:nth-child(4) ul.search_cate_list li.search_cate_item span.item_text")
memory_capacity_list = [element.text for element in memory_capacity]

chosen_index = choose_one("메모리 용량을 골라주세요.", memory_capacity_list)
chosen_memory_capacity = memory_capacity_list[chosen_index] + " " # 뒤에 공백이 있음
print(f"선택한 메모리 용량: {chosen_memory_capacity}")

# 메모리 용량 체크박스 클릭
click_checkbox(chosen_memory_capacity)

# 조회된 메모리 목록 가져오기
products = parse_product()

########################## 그래픽카드 ##########################

# 그래픽카드 카테고리 클릭
change_category("그래픽카드")

# 그래픽카드 제조사 가져오기
chosen_maker = choose_maker("그래픽카드 제조사를 골라주세요.")

# 칩셋 제조사 더보기 버튼 클릭
more_button = visibility_element("div.search_option_item:nth-child(2) button.btn_item_more")
browser.execute_script("arguments[0].click();", more_button)
time.sleep(1)

# 칩셋 제조사 가져오기
chipset_maker = visibility_elements_browser("div.search_option_item:nth-child(2) ul.search_cate_list li.search_cate_item span.item_text")
chipset_maker_list = [element.text for element in chipset_maker]

chosen_index = choose_one("칩셋 제조사를 골라주세요.", chipset_maker_list)
chosen_chipset_maker = chipset_maker_list[chosen_index] + " " # 뒤에 공백이 있음
print(f"선택한 사용장치: {chosen_chipset_maker}")

# 칩셋 제조사 체크박스 클릭
click_checkbox(chosen_chipset_maker)

# 조회된 그래픽카드 목록 가져오기
products = parse_product()

########################## ssd ##########################

# ssd 카테고리 클릭
change_category("ssd")

# ssd 제조사 가져오기
chosen_maker = choose_maker("ssd 제조사를 골라주세요.")

# 용량 더보기 버튼 클릭
more_button = visibility_element("div.search_option_item:nth-child(5) button.btn_item_more")
browser.execute_script("arguments[0].click();", more_button)
time.sleep(1)

# 용량 가져오기
ssd_capacity = visibility_elements_browser("div.search_option_item:nth-child(5) ul.search_cate_list li.search_cate_item span.item_text")
ssd_capacity_list = [element.text for element in ssd_capacity]

chosen_index = choose_one("용량을 골라주세요.", ssd_capacity_list)
chosen_ssd_capacity = ssd_capacity_list[chosen_index] + " " # 뒤에 공백이 있음
print(f"선택한 용량: {chosen_ssd_capacity}")

# 용량 체크박스 클릭
click_checkbox(chosen_ssd_capacity)

# 조회된 ssd 목록 가져오기
products = parse_product()

########################## 케이스 ##########################

# 케이스 카테고리 클릭
change_category("케이스")

# 케이스 제조사 가져오기
chosen_maker = choose_maker("케이스 제조사를 골라주세요.")

# 제품 분류 더보기 버튼 클릭
more_button = visibility_element("div.search_option_item:nth-child(2) button.btn_item_more")
browser.execute_script("arguments[0].click();", more_button)
time.sleep(1)

# 제품 분류 가져오기
product_classify = visibility_elements_browser("div.search_option_item:nth-child(2) ul.search_cate_list li.search_cate_item span.item_text")
product_classify_list = [element.text for element in product_classify]

chosen_index = choose_one("제품 분류를 골라주세요.", product_classify_list)
chosen_product_classify = product_classify_list[chosen_index] + " " # 뒤에 공백이 있음
print(f"선택한 제품 분류: {chosen_product_classify}")

# 제품 분류 체크박스 클릭
click_checkbox(chosen_product_classify)

# 조회된 케이스 목록 가져오기
products = parse_product()

########################## 파워 ##########################

# 파워 카테고리 클릭
change_category("파워")

# 파워 제조사 가져오기
chosen_maker = choose_maker("파워 제조사를 골라주세요.")

# 제품 분류 더보기 버튼 클릭
more_button = visibility_element("div.search_option_item:nth-child(2) button.btn_item_more")
browser.execute_script("arguments[0].click();", more_button)
time.sleep(1)

# 제품 분류 가져오기
product_classify = visibility_elements_browser("div.search_option_item:nth-child(2) ul.search_cate_list li.search_cate_item span.item_text")
product_classify_list = [element.text for element in product_classify]

chosen_index = choose_one("제품 분류를 골라주세요.", product_classify_list)
chosen_product_classify = product_classify_list[chosen_index] + " " # 뒤에 공백이 있음
print(f"선택한 제품 분류: {chosen_product_classify}")

# 제품 분류 체크박스 클릭
click_checkbox(chosen_product_classify)

# 정격출력 더보기 버튼 클릭
more_button = visibility_element("div.search_option_item:nth-child(3) button.btn_item_more")
browser.execute_script("arguments[0].click();", more_button)
time.sleep(1)

# 정격출력 가져오기
rated_power = visibility_elements_browser("div.search_option_item:nth-child(3) ul.search_cate_list li.search_cate_item span.item_text")
rated_power_list = [element.text for element in rated_power]

chosen_index = choose_one("정격출력을 골라주세요.", rated_power_list)
chosen_rated_power = rated_power_list[chosen_index] + " " # 뒤에 공백이 있음
print(f"선택한 정격출력: {chosen_rated_power}")

# 정격출력 체크박스 클릭
click_checkbox(chosen_rated_power)

# 80PLUS인증 더보기 버튼 클릭
more_button = visibility_element("div.search_option_item:nth-child(4) button.btn_item_more")
browser.execute_script("arguments[0].click();", more_button)
time.sleep(1)

# 80PLUS인증 가져오기
eighty_plus_certification = visibility_elements_browser("div.search_option_item:nth-child(4) ul.search_cate_list li.search_cate_item span.item_text")
eighty_plus_certification_list = [element.text for element in eighty_plus_certification]

chosen_index = choose_one("80PLUS인증을 골라주세요.", eighty_plus_certification_list)
chosen_eighty_plus_certification = eighty_plus_certification_list[chosen_index] + " " # 뒤에 공백이 있음
print(f"선택한 80PLUS인증: {chosen_eighty_plus_certification}")

# 80PLUS인증 체크박스 클릭
click_checkbox(chosen_eighty_plus_certification)

# 조회된 파워 목록 가져오기
products = parse_product()

time.sleep(3)

browser.close()