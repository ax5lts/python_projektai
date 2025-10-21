
import pyttsx3

engine = pyttsx3.init()
while True:
    voices = engine.getProperty('voices')
    text = input("Įvesk tekstą arba parašyk exit: ")
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)
    if text.lower() == "exit":
        break
    engine.say(text)
    engine.runAndWait()


