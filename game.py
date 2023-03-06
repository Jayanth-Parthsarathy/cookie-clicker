from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
timeout = time.time() + 60*5
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]
time_check = time.time()+5
cookie = driver.find_element(By.ID, 'cookie')
while True:
    cookie.click()
    if time.time()>time_check:
        money_element = driver.find_element(By.ID, 'money')
        money = money_element.text
        if ',' in money:
            money = money.replace(',','')
        money = int(money)
        store = driver.find_elements(By.CSS_SELECTOR, '#store b')
        store_text_list = []
        store_text = []
        for item in store:
            store_text_list.append(item.text.strip().split("-"))
        for item in store_text_list:
            if item[0]!="":
                store_text.append(int(item[1].replace(',','')))
        store_dict = {}
        for i in range(len(store_text)):
            store_dict[store_text[i]] = item_ids[i]
        affordable_costs = {}
        # print(store_text)
        for cost, id in store_dict.items():
            if(money>cost):
                affordable_costs[cost] = id
        to_purchase = max(affordable_costs)
        item_to_purchase = affordable_costs[to_purchase]
        item_to_purchase = driver.find_element(By.ID, item_to_purchase)
        item_to_purchase.click()
        time_check = time.time()+5
        # print(store_text)
    if time.time()>timeout:
        break
