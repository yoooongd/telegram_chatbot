from flask import Flask,request
app = Flask(__name__)

import os
import random
import requests

token = os.getenv("TELE_TOKEN")
naver_id = os.getenv("NAVER_ID")
naver_secret = os.getenv("NAVER_SECRET")

api_url="https://api.hphk.io/telegram"
#api_url="https://api.telegram.org"

@app.route("/")
def hello():
    return "Hello World!"
    
@app.route(f"/{token}",methods=["POST"])    
def telegram():
    msg_info = request.get_json()
    
    #메시지를 보낸 사람의 아이디
    chat_id = msg_info.get("message").get("from").get("id")
    #딕셔너리에서 키 벨류 값을 가져올 때 대괄호를 활용한다면 error
    #get을 사용하면 없어도 none
    
    
    #사용자가 보낸 메시지
    text = msg_info.get("message").get("text")
    return_text="임시"
    if msg_info.get("message").get("photo") is not None:
        #사진이 있을 때
        file_id = msg_info.get("message").get("photo")[-1].get("file_id")
        file_res = requests.get(f"{api_url}/bot{token}/getFile?file_id={file_id}")
        file_path = file_res.json().get("result").get("file_path")
        file_url = f"{api_url}/file/bot{token}/{file_path}"
        #return_text=file_url
        
        real_file=requests.get(file_url,stream=True)
        headers = {
                "X-Naver-Client-Id":naver_id,
                "X-Naver-Client-Secret":naver_secret
            }
        naver_url = "https://openapi.naver.com/v1/vision/celebrity"
        clova = requests.post(naver_url,headers=headers,files={"image":real_file.raw.read()})
        
        
        if clova.json().get("info").get("faceCount"):
            #사람이 인식 될 때
            clova_return=clova.json().get("faces")[0].get("celebrity")
            return_text=clova_return.get('value')
        else:
            #사람이 인식되지 않을 때
            return_text="사람이 없어요"
        
    else:
        #사진이 없을 때
        if text == "로또":
            return_text = sorted(random.sample(range(1,46),6))
        elif text == "메뉴":
            menu_list = ["양자강","명동칼국수","김밥카페","시골집"]
            return_text = random.choice(menu_list)
        elif text[0:3] == "번역 ":
            headers = {
                "X-Naver-Client-Id":naver_id,
                "X-Naver-Client-Secret":naver_secret
            }
            naver_url = "https://openapi.naver.com/v1/papago/n2mt"
            data = {
                "source":"ko",
                "target":"en",
                "text":text[3:]
            }
            papago = requests.post(naver_url,headers=headers,data=data)
            return_text = papago.json().get("message").get("result").get("translatedText")
        else:
            return_text = "없는명령어입니다."
    
    return_url = f"{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={return_text}"
    requests.get(return_url)
    
    return '',200

    
if __name__ == "__main__":
    app.run(debug=True,host=os.getenv("IP","0.0.0.0"),port=int(os.getenv("PORT",8080)))