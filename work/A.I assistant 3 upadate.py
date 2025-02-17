import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
import json

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change the index to select a different voice

weather_api_key = '15a9a19ff395d7c8f8746988654e9e75'  # Replace with your weather API key


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("How can I help you?")


def get_weather(city):
    base_url = f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no'
    response = requests.get(base_url)
    data = json.loads(response.text)

    if 'error' in data:
        return "Sorry, I couldn't fetch the weather information."

    temperature = data['current']['temp_c']
    condition = data['current']['condition']['text']
    humidity = data['current']['humidity']
    wind_speed = data['current']['wind_kph']

    weather_info = f"The current weather in {city} is {condition} with a temperature of {temperature} degrees Celsius. " \
                   f"The humidity is {humidity}% and the wind speed is {wind_speed} kilometers per hour."

    return weather_info


r = sr.Recognizer()


def takeCommand():
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        print("Audio captured")

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "None"

def send_email(to, subject, body):
    # Configure your email settings
    email_address = 'slovesh52@gmail.com'
    email_password = os.getenv('EMAIL_PASSWORD')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)

    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(email_address, to, message)
    server.quit()


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'who are you' in query:
            print("Assistant")
            speak('I am a virtual assistant and I was coded by a coder.')

        if 'wikipedia' in query:
            speak('Searching on Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")

        elif 'play music' in query:
            music_dir = 'C:\\Users\\niles\\OneDrive\\Desktop\\MUSIC'
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("No songs found in the directory.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'search for' in query or 'google search' in query:
            search_term = query.split('for', 1)[1].strip()
            url = f"https://www.google.com/search?q={search_term}"
            webbrowser.get().open(url)

        elif 'open code' in query:
            codePath = "D:\Project 2\A.I assistant 3 upadate.py"
            os.startfile(codePath)

        elif 'good' in query:
            speak("That's great!")

        elif 'weather' in query:
            city = 'harayana'  # Replace with your desired city
            weather_info = get_weather(city)
            speak(weather_info)
            print(weather_info)

        elif 'send email' in query:
            try:
                speak("To whom should I send the email?")
                recipient = takeCommand().lower()
                speak("What should be the subject of the email?")
                email_subject = takeCommand().lower()
                speak("What message should I include in the email?")
                email_body = takeCommand().lower()

                send_email(recipient, email_subject, email_body)
                speak("Email sent successfully!")
            except Exception as e:
                speak("Sorry, I couldn't send the email. Please try again.")

        elif 'stop working' in query or 'stop' in query:
            speak("Goodbye!")
            break
