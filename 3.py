import tkinter as tk
import requests
import json
import base64
import tkinter.messagebox

API_KEY = "cVAjjdIIgsJ4taIZEgEJgNhm"
SECRET_KEY = "MhHxwhDTmbdbHZiKFsDcQNuw3Ckv8loJ"


def translate_audio():
    url = "https://aip.baidubce.com/rpc/2.0/mt/v2/speech-translation?access_token=" + get_access_token()

    with open("speech.wav", "rb") as audio_file:
        audio_data = audio_file.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

    payload = {
        "from": "zh",
        "to": "en",
        "format": "pcm",
        "voice": audio_base64
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_json = response.json()

    if "error_code" in response_json:
        error_msg = response_json.get("error_msg")
        result_label.config(text=f"Translation error: {error_msg}")
    else:
        translation_result = response_json["result"]["source"]
        translation_result2 = response_json["result"]["target"]
        result_label.config(text=translation_result)
        result_label2.config(text=translation_result2)


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


# 创建GUI窗口
window = tk.Tk()
window.title("语音翻译")
window.geometry("1000x500")

# 创建按钮和标签

translate_button = tk.Button(window, text="翻译", command=translate_audio,width=10, height=2)
translate_button.pack(pady=20)
result_label = tk.Label(window, text="")
result_label.pack()

result_label2 = tk.Label(window, text="")
result_label2.pack()

# 运行GUI主循环
window.mainloop()
