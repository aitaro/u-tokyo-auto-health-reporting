from selenium import webdriver
import yaml
import os
import time
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

# main
config = yaml.safe_load(open('config.yaml').read())
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

if not email:
    raise ValueError('no email in env')
if not password:
    raise ValueError('no password in env')

destination_str = config.get('destination')
destination = None
if destination_str == 'hongo':
    destination = 0
elif destination_str == 'komaba':
    destination = 1
elif destination_str == 'kashiwa':
    destination = 2
elif destination_str == 'other':
    destination = 3
else:
    raise ValueError('invalid destination')

stay = config.get('stay')
if not stay:
    raise ValueError('invalid stay')

# Chromeで操作する場合
# 全体的に日本語で始まる値がうまいこといかない印象がある。
driver.get('https://forms.office.com/Pages/ResponsePage.aspx?id=T6978HAr10eaAgh1yvlMhF__kSldrNpNvIWhwdsjjRJURUZEVjlIWjM1VjhXMlVaRVJaWVpEVjJZVCQlQCN0PWcu')
time.sleep(10)
driver.find_element_by_name("loginfmt").send_keys(email)
driver.find_element_by_id("idSIButton9").click()

time.sleep(10)
driver.find_element_by_name("Password").send_keys(password)
driver.find_element_by_id("submitButton").click()

time.sleep(10)
driver.find_element_by_id("idBtn_Back").click()

time.sleep(10)
driver.find_element_by_css_selector(
    "input[aria-label='ECCSクラウドメール(共通ID@g.ecc.u-tokyo.ac.jp)宛に送信']").click()
time.sleep(2)
driver.find_elements_by_css_selector("input[type='checkbox']")[
    destination].click()
time.sleep(2)
driver.find_element_by_css_selector(
    "input[maxlength='4000']").send_keys(stay)
time.sleep(2)
driver.find_elements_by_css_selector("input[type='radio']")[2].click()
time.sleep(5)
driver.find_elements_by_css_selector("input[type='radio']")[6].click()
driver.find_element_by_css_selector("button.__submit-button__").click()


driver.quit()
