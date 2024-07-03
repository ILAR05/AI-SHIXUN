import os
import time
import wave
import audioop
import base64
from pyaudio import PyAudio, paInt16
import wenet

framerate = 16000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampWidth = 2  # 采样宽度2bytes
FILEPATH = 'speech.wav'


def save_wave_file(filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampWidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()


def my_record():
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=channels,
                     rate=framerate, input=True, frames_per_buffer=num_samples)
    my_buf = []
    t = time.time()
    print('正在录音...')

    while time.time() < t + 5:  # 秒
        string_audio_data = stream.read(num_samples)
        my_buf.append(string_audio_data)
    print('录音结束.')
    save_wave_file(FILEPATH, my_buf)
    stream.close()


def wenet_work():
    model = wenet.load_model('chinese')
    result = model.transcribe(FILEPATH)
    return result['text']


def convert_wav_to_txt(wav_file, txt_file):
    with wave.open(wav_file, 'rb') as wf:
        frames = wf.readframes(wf.getnframes())
        audio_data = audioop.lin2lin(frames, wf.getsampwidth(), 2)  # 转换采样宽度为16-bit

    # 使用Base64编码将音频数据转换为文本格式
    encoded_data = base64.b64encode(audio_data)

    with open(txt_file, 'w', encoding='utf-8') as tf:
        tf.write(encoded_data.decode('utf-8'))


def get_audio(file):
    with open(file, 'rb') as f:
        data = f.read()
    return data


if __name__ == '__main__':
    flag = 'y'
    while flag.lower() == 'y':
        my_record()

        speech = get_audio(FILEPATH)

        print(wenet_work())

        txt_file = FILEPATH.replace('.wav', '.txt')
        convert_wav_to_txt(FILEPATH, txt_file)
        print('转换为文本文件:', txt_file)

        flag = input('Continue?(y/n):')

