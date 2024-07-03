from tkinter import scrolledtext

import requests
import json
import tkinter as tk

import wenet

API_KEY = "MFPcLPeFZoyfnYKpQ9hP7nOM"
SECRET_KEY = "FCPI5CDzoUMwcrcoZSZ1Zl06bbfl5wjx"


def trans(res):
    url = "https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=" + get_access_token()

    payload = json.dumps({
        "q": res,  # 添加要翻译的文本
        "from": "zh",
        "to": "en"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()['result']['trans_result'][0]['dst']
    else:
        print(f"Error: {response.status_code}, {response.text}")


def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return requests.post(url, params=params).json().get("access_token")


# 创建GUI窗口
window = tk.Tk()
window.title("语音识别与翻译")
window.geometry("800x600")

# 创建左右布局的框架
frame = tk.Frame(window)
frame.pack(fill=tk.BOTH, expand=True)

# 创建左侧滚动文本框
result_scroll = scrolledtext.ScrolledText(frame, width=50, height=30)
result_scroll.pack(side=tk.LEFT, padx=5, pady=10)

# 创建右侧滚动文本框
translation_scroll = scrolledtext.ScrolledText(frame, width=50, height=30)
translation_scroll.pack(side=tk.RIGHT, padx=5, pady=10)

# 创建翻译按钮
translate_button = tk.Button(window, text="翻译", width=10, height=2)
translate_button.pack(pady=20)


def wenet_work():
    model = wenet.load_model('chinese')
    result = model.transcribe('speech.wav')
    return result['text']
    pass


def translate_wenet_output():
    wenet_output = wenet_work()
    translation = trans(wenet_output)
    result_scroll.delete(1.0, tk.END)
    result_scroll.insert(tk.END, wenet_output)
    translation_scroll.delete(1.0, tk.END)
    translation_scroll.insert(tk.END, translation)


translate_button.config(command=translate_wenet_output)

# 运行GUI主循环
window.mainloop()
