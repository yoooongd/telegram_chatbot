import requests
import random
import os
from bs4 import BeautifulSoup

token = os.getenv("TELE_TOKEN")
chat_id = "759695019"
#url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=testChatbot"
url = f"https://api.hphk.io/telegram/bot{token}/sendMessage?chat_id={chat_id}&text="

# sise_url = "https://finance.naver.com/sise/"
# sise_html = requests.get(sise_url).text
# sise_soup = BeautifulSoup(sise_html,"html.parser")
# sise = sise_soup.select_one("#KOSPI_now").text

# menu_list = ["김밥카페","시골집","강남목장","양자강"]
# pick = random.choice(menu_list)

numbers = range(1,46)
pick = random.sample(numbers,6)

res = requests.get(url+str(pick))
print(res)
#print(url)