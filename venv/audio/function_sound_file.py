from playsound import playsound


def function_sound(filename):
    try:
        playsound(filename)
    except Exception:
        pass

# def main():
#     openaiurl = "https://api.openai.com/v1"
#
#     headers = {"Authorization": f"Bearer YOUR API KEY"}
#
#     # implement a counter
#     while True:
#
#     ###################################################################
#     ###           1. Record using microphone                        ###
#     ###################################################################
#
#         print("[-] Record audio using microphone")
#
#         # obtain audio from the microphone
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             r.adjust_for_ambient_noise(source)
#             print("Say something!")
#             audio = r.listen(source)
#
#         folder = "./audio"
#         filename = "microphone-results"
#         audio_file_path = f"{folder}/{filename}.wav"
#
#         if not os.path.exists(folder):
#             os.mkdir(folder)
#
#         # write audio to a WAV file
#         print(f"Generating WAV file, saving at location: {audio_file_path}")
#         with open(audio_file_path, "wb") as f:
#             f.write(audio.get_wav_data())
#
#         ###################################################################
#         ###      2. Call to Whisper API's and getting result            ###
#         ###################################################################
#
#         print("[-] Call to Whisper API's to get the STT response")
#
#         url = f"{openaiurl}/audio/transcriptions"
#
#         data = {
#             "model": "whisper-1",
#             "file": audio_file_path,
#         }
#         files = {
#             "file": open(audio_file_path, "rb")
#         }
#
#         response = requests.post(url, files=files, data=data, headers=headers)
#         print(response.json())
#         print("Status Code", response.status_code)
#         speech_to_text = response.json()["text"]
#         print("Response from Whisper API's", speech_to_text)
#
#         ###################################################################
#         ###   3. Query ChatGPT model with the text get the response     ###
#         ###################################################################
#
#         print("[-] Querying ChatGPT model with the STT response data")
#         url = f"{openaiurl}/chat/completions"
#
#         data = {
#             "model": "gpt-3.5-turbo",
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": speech_to_text
#                 }
#             ]
#         }
#
#         response = requests.post(url, json=data, headers=headers)
#
#         print("Status Code", response.status_code)
#         chatgpt_response = response.json()["choices"][0]["message"]["content"]
#         print("Response from ChatGPT model ", chatgpt_response)
#
#         ###################################################################
#         ###      4. Try to convert TTS from the response                ###
#         ###################################################################
#
#         print("[-] Try to convert TTS from the response")
#
#         engine = pyttsx3.init()
#         engine.setProperty('rate', 175)
#
#         print("Converting text to speech...")
#         engine.say(chatgpt_response)
#
#         engine.runAndWait()
#         engine.stop()
#
#         break
