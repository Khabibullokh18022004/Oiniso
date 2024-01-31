import os
import time
import GoogleCloud
import speech_recognition as sr
import requests
import pyttsx3
import wave
from playsound import playsound
from MohirAi import MohirAi


def select_language():
    playsound('Salomlash.wav')
    playsound('Privetstvie.mp3')
    playsound('Greeting.mp3')

    ch = int(input("choice:"))

    if ch == 1:
        uzbek_bot()
    elif ch == 2:
        russian_bot()
    elif ch == 3:
        english_bot()
    else:
        select_language()


def uzbek_bot():
    openaiurl = "https://api.openai.com/v1"

    headers = {"Authorization": f"Bearer YOUR API KEY"}

    playsound('Bo\'shlash.wav')

    mohir = MohirAi(api_key="YOUR MOHIRAI API KEY ")

    while True:

        ###################################################################
        ###           1. Record using microphone                        ###
        ###################################################################

        print("[-] Record audio using microphone")

        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            audio = r.listen(source)

        audio_file_path = "savol.wav"

        # write audio to a WAV file
        print(f"Generating WAV file, saving at location: {audio_file_path}")
        with open(audio_file_path, "wb") as f:
            f.write(audio.get_wav_data())

        ###################################################################
        ###      2. Call to Whisper API's and getting result            ###
        ###################################################################

        print("[-] Call to MohirAI API's to get the STT response")

        speech_to_text = mohir.stt(audio_file_path)

        print("Response from MohirAI API's", speech_to_text)

        if speech_to_text == '.':
            continue

        ###################################################################
        ###   3. Query ChatGPT model with the text get the response     ###
        ###################################################################

        print("[-] Querying ChatGPT model with the STT response data")
        url = f"{openaiurl}/chat/completions"

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": f'''
                    Представь, что ты работник колл-цетра узбекского банка. Давай клиентам краткие инструкции о том, 
                    как решить их проблемы. При необходимости, можешь попросить данные клиента, для открытия заявки.
                    Твоя цель- помогать клиентам в решении их проблем касаемо их вопросов с сервисом банка.
                    Кстати говоря работаешь ты в Агробанке, который находится в Узбекистане. Не говори клиентам ничего лишнего,
                    что не касается твоей деятельности как работника колл-цетра банка. 
                    Пожалуйста, имей ввиду, что ты представитель всего банка и не натвори глупостей.
                    Отвечай короткими ответами на вопросы клиентов. В ответе включи только важную часть ответа,
                    без тела вопроса или же моего промпта.
                    Ответь на узбекском языке! Это очень важно.
                    Ниже прикрепляю сам вопрос клиента: 
                    {speech_to_text}
                    '''
                }
            ]
        }

        response = requests.post(url, json=data, headers=headers)

        print("Status Code", response.status_code)
        chatgpt_response = response.json()["choices"][0]["message"]["content"]
        print("Response from ChatGPT model ", chatgpt_response)

        ###################################################################
        ###      4. Try to convert TTS from the response                ###
        ###################################################################

        print("[-] Try to convert TTS from the response")
        mohir.tts(text=chatgpt_response, model="dilfuza", mood="happy", filename="javob")


def russian_bot():
    playsound('Nachalo.mp3')

    openaiurl = "https://api.openai.com/v1"

    headers = {"Authorization": f"Bearer YOUR API KEY"}

    # implement a counter
    while True:

        ###################################################################
        ###           1. Record using microphone                        ###
        ###################################################################

        print("[-] Record audio using microphone")

        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            audio = r.listen(source)

        audio_file_path = "vopros.mp3"

        # write audio to a WAV file
        print(f"Generating WAV file, saving at location: {audio_file_path}")
        with open(audio_file_path, "wb") as f:
            f.write(audio.get_wav_data())

        ###################################################################
        ###      2. Call to Whisper API's and getting result            ###
        ###################################################################

        print("[-] Call to Whisper API's to get the STT response")

        url = f"{openaiurl}/audio/transcriptions"

        data = {
            "model": "whisper-1",
            "file": audio_file_path,
        }
        files = {
            "file": open(audio_file_path, "rb")
        }

        response = requests.post(url, files=files, data=data, headers=headers)
        print(response.json())
        print("Status Code", response.status_code)
        speech_to_text = response.json()["text"]
        print("Response from Whisper API's", speech_to_text)

        if speech_to_text == '.':
            continue

        ###################################################################
        ###   3. Query ChatGPT model with the text get the response     ###
        ###################################################################

        print("[-] Querying ChatGPT model with the STT response data")
        url = f"{openaiurl}/chat/completions"

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": f'''
                    Представь, что ты работник колл-цетра узбекского банка. Давай клиентам краткие инструкции о том, 
                    как решить их проблемы. При необходимости, можешь попросить данные клиента, для открытия заявки.
                    Твоя цель- помогать клиентам в решении их проблем касаемо их вопросов с сервисом банка.
                    Кстати говоря работаешь ты в Агробанке, который находится в Узбекистане. Не говори клиентам ничего лишнего,
                    что не касается твоей деятельности как работника колл-цетра банка. Пожалуйста, имей ввиду, 
                    что ты представитель всего банка и не натвори глупостей. Отвечай короткими ответами на вопросы клиентов.
                    В ответе включи только важную часть ответа, без тела вопроса или же этого промпта. Пиши ответы в женском лице. 
                    Ниже прикрепляю сам вопрос клиента: 
                    {speech_to_text}
                    '''
                }
            ]
        }

        response = requests.post(url, json=data, headers=headers)

        print("Status Code", response.status_code)
        chatgpt_response = response.json()["choices"][0]["message"]["content"]
        print("Response from ChatGPT model ", chatgpt_response)

        ###################################################################
        ###      4. Try to convert TTS from the response                ###
        ###################################################################

        print("[-] Try to convert TTS from the response")

        GoogleCloud.speak_russian(chatgpt_response, 'otvet')


def english_bot():
    playsound('Start.mp3')

    openaiurl = "https://api.openai.com/v1"

    headers = {"Authorization": f"Bearer YOUR API KEY"}

    # implement a counter
    while True:

        ###################################################################
        ###           1. Record using microphone                        ###
        ###################################################################

        print("[-] Record audio using microphone")

        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            audio = r.listen(source)

        audio_file_path = "question.mp3"

        # write audio to a WAV file
        print(f"Generating WAV file, saving at location: {audio_file_path}")
        with open(audio_file_path, "wb") as f:
            f.write(audio.get_wav_data())

        ###################################################################
        ###      2. Call to Whisper API's and getting result            ###
        ###################################################################

        print("[-] Call to Whisper API's to get the STT response")

        url = f"{openaiurl}/audio/transcriptions"

        data = {
            "model": "whisper-1",
            "file": audio_file_path,
        }
        files = {
            "file": open(audio_file_path, "rb")
        }

        response = requests.post(url, files=files, data=data, headers=headers)
        print(response.json())
        print("Status Code", response.status_code)
        speech_to_text = response.json()["text"]
        print("Response from Whisper API's", speech_to_text)

        if speech_to_text == '.':
            continue

        ###################################################################
        ###   3. Query ChatGPT model with the text get the response     ###
        ###################################################################

        print("[-] Querying ChatGPT model with the STT response data")
        url = f"{openaiurl}/chat/completions"

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": f'''
                    Представь, что ты работник колл-цетра узбекского банка. Давай клиентам краткие инструкции о том, 
                    как решить их проблемы. При необходимости, можешь попросить данные клиента, для открытия заявки.
                    Твоя цель- помогать клиентам в решении их проблем касаемо их вопросов с сервисом банка.
                    Кстати говоря работаешь ты в Агробанке, который находится в Узбекистане. Не говори клиентам ничего лишнего,
                    что не касается твоей деятельности как работника колл-цетра банка. Пожалуйста, имей ввиду, 
                    что ты представитель всего банка и не натвори глупостей. Отвечай короткими ответами на вопросы клиентов.
                    В ответе включи только важную часть ответа, без тела вопроса или же этого промпта.
                    Пиши все ответы на английском, так как это очень важно! 

                    Ниже прикрепляю сам вопрос клиента: 
                    {speech_to_text}
                    '''
                }
            ]
        }

        response = requests.post(url, json=data, headers=headers)

        print("Status Code", response.status_code)
        chatgpt_response = response.json()["choices"][0]["message"]["content"]
        print("Response from ChatGPT model ", chatgpt_response)

        ###################################################################
        ###      4. Try to convert TTS from the response                ###
        ###################################################################

        print("[-] Try to convert TTS from the response")

        GoogleCloud.speak_english(chatgpt_response, 'answer')


if __name__ == '__main__':
    select_language()
