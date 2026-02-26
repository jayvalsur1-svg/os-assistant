import speech_recognition as sr
import webbrowser
import subprocess
import musicplaylist
import requests
import pyttsx3
import importlib
from groq import Groq
import time
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapikey = ""
weathearapikey=""
groqaiapikey=""
def ask_llama(text):
    client = Groq(api_key=groqaiapikey)
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are Jarvis, a friendly humanoid buddy. Keep answers short."},
                {"role": "user", "content": text}
            ]
        )
        response = completion.choices[0].message.content
        speak(response)
    except Exception as e:
        print(f"Groq Error: {e}")
        speak("I'm having trouble connecting to my brain right now.")


def speak(text):
    print(f"Assistant: {text}")
    try:
        importlib.reload(pyttsx3) 
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        del engine
    except Exception as e:
        print(f"TTS Failed: {e}")
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=10)
    return recognizer.recognize_google(audio)

def processcommand(command):
    print("processcommand got:", command)
    command = command.lower()

    if "google" in command:
        webbrowser.open("https://google.com")
    elif "intro"in command:
        speak("My name is jarvis")
        speak("I am operating system controller ")
        speak("I am able process your command like open Youtube,open camera ,open chrome,open classroom and more")
        speak("I also provide you i latest news")
        speak("I am also able to see weather according your Location")
        speak("if command not recognize so that command calling llm as prompt")
        speak("how may i serve you")
    elif "assistant" in command:
        speak("Yes")
        text = listen()
        speak("Heard:", text)
        processcommand(text)
    elif "youtube" in command:
        speak("Youtube opening...")
        webbrowser.open("https://youtube.com")

    elif "calculator" in command:
        speak("calculator opening..")
        subprocess.Popen("calc.exe")

    elif "camera" in command:
        speak("camera opening")
        subprocess.Popen("start microsoft.windows.camera:", shell=True)
    elif "notepad" in command:
        speak("notepad opening")
        subprocess.Popen(r"C:\Windows\System32\notepad.exe", shell=True)
    elif "brave" in command:
        speak("brave opening")
        subprocess.Popen(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe", shell=True)

    elif "chrome" in command:
        speak("google chrome opening")
        subprocess.Popen("start chrome", shell=True)

    elif "google_classroom" in command:
        speak("google_classroom")
        subprocess.Popen("start chrome https://classroom.google.com/?lfhs=2", shell=True)
    elif "terminal" in command:
        speak("terminal is opening ")
        subprocess.Popen(r"C:\Windows\System32\cmd.exe",shell=True)
    elif "wordpad" in command:
        speak("Wordpad opening")
        subprocess(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Wordpad.lnk",shell=True)
    elif "paint" in command:
        speak("paint opening")
        subprocess.Popen(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Paint.lnk",shell=True)

    elif "word" in command:
        speak("msword Tool opening")
        subprocess.Popen(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word 2016.lnk",shell=True)
    elif "powerpoint" in command:
        speak("powerpoint Tool opening")
        subprocess.Popen(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint 2016.lnk",shell=True)
    elif "excel" in command:
        speak("excel Tool opening")
        subprocess.Popen(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel 2016.lnk",shell=True)

    elif command.startswith("play"):
        speak(f"Your song {command} started to playing")
        song = command.replace("play", "").strip()

        normalized_library = {k.lower(): v for k, v in musicplaylist.library.items()}

        if song in normalized_library:
            webbrowser.open(normalized_library[song])
        else:
            speak("Song not found")
    elif "music library" in command:
        for song, url in musicplaylist.library.items():
            speak(f"Playing {song}")
            webbrowser.open(url)
            time.sleep(200) 
        speak("Playlist opened in browser")
    elif "news" in command:
        url = f"https://gnews.io/api/v4/top-headlines?category=general&lang=en&apikey={newsapikey}"

        try:
            response = requests.get(url)
            data = response.json()

            if "articles" in data and data["articles"]:
                speak("Here are the top news headlines.")
                for article in data["articles"][:5]:
                    speak(article["title"])
            else:
                speak("No news found.")

        except Exception as e:
            print("News Error:", e)
            speak("Unable to fetch news.")
    elif "weather" in command:
        CITY = 'Surat'
        BASE_URL = "http://api.weatherapi.com/v1/current.json"
        params = {
            'key': weathearapikey,
            'q': CITY,
            'aqi': 'no'  
        }
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            location = data['location']['name']
            region = data['location']['region']
            temp_c = data['current']['temp_c']
            condition = data['current']['condition']['text']
            speak(f"Weather in {location}, {region}:")
            speak(f"Temperature: {temp_c}°C")
            speak(f"Condition: {condition}")

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as err:
            print(f"An error occurred: {err}")
    else:
            ask_llama(command)

if __name__ == "__main__":
    speak("Initializing Assistant")

    while True:
        try:
            print("0 for text input, 1 for voice input")
            j = input("enter value :- ")

            if j == "0":
                text = input("Input command to assistant: ")
                processcommand(text)

            elif j == "1":
                text = listen()
                print("Heard:", text)
                processcommand(text)

        except sr.UnknownValueError:
            print("Could not understand audio")

        except Exception as e:
            print("Error:", e)