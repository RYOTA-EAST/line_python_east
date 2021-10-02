import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ローカルに保存しているChrome Driverを指定 (※デプロイするときはコメントアウトする)
# driver_path = "/Users/ryotahigashi/chromedriver" ###あなたが対応する箇所（記入例：C:\Users\desktop\chromedriver.exe）

# Heroku上のChrome Driverを指定(※デプロイするときはコメントを外す)
driver_path = '/app/.chromedriver/bin/chromedriver'

# Headless Chromeをあらゆる環境で起動させるオプション
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized')
options.add_argument('--headless')

#クローラーの起動
driver = webdriver.Chrome(executable_path = driver_path, chrome_options = options)

#Yahooファイナンスへアクセス
driver.get('https://finance.yahoo.co.jp/')

#ヘッドラインニュースの情報抽出
elements = driver.find_element_by_xpath('//*[@id="ytopContentIn"]')
message = elements.text

# ブラウザを終了する
driver.quit()

# LINE通知用に定義した関数
def line_notify(message):
	line_notify_token =  os.environ['LINE_NOTIFY_TOKEN']
	line_notify_api = 'https://notify-api.line.me/api/notify'
	payload = {'message': message}
	headers = {'Authorization': 'Bearer ' + line_notify_token}
	requests.post(line_notify_api, data=payload, headers=headers)

# LINEに通知させる
line_notify(message)