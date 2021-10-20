import requests
import datetime
import os

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

url = f'https://mypytodo-ryo-east.herokuapp.com/api/todo/?status=1,2&create_user=1&deadline={now}'
res = requests.get(url)
data_json = res.json()


message = f'今は{now}\n期限切れのタスクが{len(data_json)}件あります\nhttps://mypytodo-ryo-east.herokuapp.com/'

i = 1

for data in data_json:
  message = message + f'\n({i}){data["title"]}'
  i += 1

print(message)

# LINE通知用に定義した関数
def line_notify(message):
	line_notify_token =  os.environ['LINE_NOTIFY_TOKEN']
	line_notify_api = 'https://notify-api.line.me/api/notify'
	payload = {'message': message}
	headers = {'Authorization': 'Bearer ' + line_notify_token}
	requests.post(line_notify_api, data=payload, headers=headers)

# LINEに通知させる
line_notify(message)
