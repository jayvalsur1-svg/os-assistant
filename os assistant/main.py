import speech_recognition as sr
import webbrowser
import pyttsx3
import subprocess
import musicplaylist
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapikey = "90bb150a3de202999168745503fc84ab"

def speak(text):
    print("Assistant:", text)
    engine.stop()
    engine.say(text)
    engine.runAndWait()

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

    elif "youtube" in command:
        webbrowser.open("https://youtube.com")

    elif "calculator" in command:
        subprocess.Popen("calc.exe")

    elif "camera" in command:
        subprocess.Popen("start microsoft.windows.camera:", shell=True)

    elif "chrome" in command:
        subprocess.Popen("start chrome", shell=True)

    elif "classroom" in command:
        subprocess.Popen("start chrome https://classroom.google.com/?lfhs=2", shell=True)

    elif command.startswith("play"):
        song = command.replace("play", "").strip()

        normalized_library = {k.lower(): v for k, v in musicplaylist.library.items()}

        if song in normalized_library:
            webbrowser.open(normalized_library[song])
        else:
            speak("Song not found")

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

    else:
        speak("Command not recognized")

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