from selenium import webdriver
import yaml
import os
import time
from fake_useragent import UserAgent


chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--window-size=1280x1696')
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--hide-scrollbars')
# chrome_options.add_argument('--enable-logging')
# chrome_options.add_argument('--log-level=0')
# chrome_options.add_argument('--v=99')
# chrome_options.add_argument('--single-process')
# chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('user-agent='+UserAgent().random)

chrome_options.binary_location = os.getcwd() + "/headless-chromium"
driver = webdriver.Chrome(os.getcwd() + "/chromedriver",
                          options=chrome_options)

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
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get('https://forms.office.com/Pages/ResponsePage.aspx?id=T6978HAr10eaAgh1yvlMhF__kSldrNpNvIWhwdsjjRJURUZEVjlIWjM1VjhXMlVaRVJaWVpEVjJZVCQlQCN0PWcu')
time.sleep(3)
driver.find_element_by_name("loginfmt").send_keys(email)
driver.find_element_by_id("idSIButton9").click()

time.sleep(3)
driver.find_element_by_name("Password").send_keys(password)
driver.find_element_by_id("submitButton").click()

time.sleep(3)
driver.find_element_by_id("idBtn_Back").click()

time.sleep(3)
driver.find_element_by_css_selector(
    "input[aria-label='ECCSクラウドメール(共通ID@g.ecc.u-tokyo.ac.jp)宛に送信']").click()
driver.find_element_by_css_selector(
    f"input[aria-label='{destination}']").click()
driver.find_element_by_css_selector(
    "input[placeholder='回答を入力してください']").send_keys(stay)

driver.find_element_by_css_selector(
    "input[aria-label='37.0度未満／Less than 37.0 degrees Celsius']").click()
time.sleep(1)
driver.find_element_by_css_selector("input[aria-label='いいえ／No']").click()
# driver.find_element_by_css_selector("button[title='送信']").click()


driver.quit()
