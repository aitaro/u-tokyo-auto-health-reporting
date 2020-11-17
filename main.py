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
    destination = '本郷地区／Hongo Area'
elif destination_str == 'komaba':
    destination = '駒場Ⅱ地区／KomabaⅡ Area　'
elif destination_str == 'kashiwa':
    destination = '柏地区／Kashiwa Area'
elif destination_str == 'other':
    destination = 'その他／Other Campus'
else:
    raise ValueError('invalid destination')

stay = config.get('stay')
if not stay:
    raise ValueError('invalid stay')

# Chromeで操作する場合
# driver = webdriver.Chrome(executable_path='chromedriver')
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
debug = driver.find_elements_by_css_selector("input[type='checkbox']")
debug[0].click()
for i in debug:
    print(i.get_attribute('value'))
time.sleep(2)
# driver.find_element_by_css_selector(
#     f"input[aria-label='{destination}']").click()
time.sleep(2)
driver.find_element_by_css_selector(
    "input[placeholder='回答を入力してください']").send_keys(stay)

driver.find_element_by_css_selector(
    "input[aria-label='37.0度未満／Less than 37.0 degrees Celsius']").click()
time.sleep(5)
driver.find_element_by_css_selector("input[aria-label='いいえ／No']").click()
# driver.find_element_by_css_selector("button[title='送信']").click()


driver.quit()
