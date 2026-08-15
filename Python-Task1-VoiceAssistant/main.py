import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import urllib.parse
import wikipedia

# -----------------------------
# INITIALIZATION
# -----------------------------

engine = pyttsx3.init()
engine.setProperty("rate", 170)

recognizer = sr.Recognizer()


# -----------------------------
# TEXT TO SPEECH
# -----------------------------

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


# -----------------------------
# LISTEN
# -----------------------------

def listen():
    with sr.Microphone() as source:

        print("\n🎤 Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

    print("🔄 Recognizing...")

    try:
        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print(f"You: {command}")

        return command.lower()

    except sr.UnknownValueError:
        print("Could not understand your voice.")
        speak("Sorry, I could not understand you.")
        return ""

    except sr.RequestError:
        print("Speech recognition service error.")
        speak("There is a problem with the speech recognition service.")
        return ""


# -----------------------------
# COMMAND FUNCTIONS
# -----------------------------

def tell_time():

    current_time = datetime.datetime.now().strftime("%I:%M %p")

    speak(f"The current time is {current_time}")


def tell_date():

    current_date = datetime.datetime.now().strftime("%d %B %Y")

    speak(f"Today's date is {current_date}")


def search_google(query):

    if not query:
        speak("What would you like me to search?")
        return

    speak(f"Searching Google for {query}")

    encoded_query = urllib.parse.quote(query)

    url = f"https://www.google.com/search?q={encoded_query}"

    webbrowser.open(url)


def search_youtube(query):

    if not query:
        speak("What would you like me to search on YouTube?")
        return

    speak(f"Searching YouTube for {query}")

    encoded_query = urllib.parse.quote(query)

    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    webbrowser.open(url)

def search_wikipedia(query):

    if not query:
        speak("What would you like me to search on Wikipedia?")
        return

    speak(f"Searching Wikipedia for {query}")

    try:
        wikipedia.set_lang("en")

        result = wikipedia.summary(
            query,
            sentences=2
        )

        print("\nWikipedia:")
        print(result)

        speak(result)

    except wikipedia.exceptions.DisambiguationError as error:

        print("Multiple results found:", error.options[:5])

        speak(
            "I found multiple results. "
            "Please be more specific."
        )

    except wikipedia.exceptions.PageError:

        speak(
            "Sorry, I could not find that information on Wikipedia."
        )

    except Exception as error:

        print("Wikipedia Error:", error)

        speak(
            "Sorry, I couldn't access Wikipedia right now."
        )


# -----------------------------
# PROCESS COMMAND
# -----------------------------

def process_command(command):

    # Greeting
    if "hello" in command or "hi" in command:

        speak("Hello! How can I help you?")


    # Time
    elif "time" in command:

        tell_time()


    # Date
    elif "date" in command:

        tell_date()


    # Open Google
    elif "open google" in command:

        speak("Opening Google.")

        webbrowser.open("https://www.google.com")


    # Open YouTube
    elif "open youtube" in command:

        speak("Opening YouTube.")

        webbrowser.open("https://www.youtube.com")

    elif "open gmail" in command:
      speak("Opening Gmail.")
      webbrowser.open("https://mail.google.com")

    elif "open github" in command:
       speak("Opening GitHub.")
       webbrowser.open("https://github.com")

    elif command.startswith("search"):

      query = command.replace("search", "", 1).strip()

      if query:
        speak(f"Searching Google for {query}")

        encoded_query = urllib.parse.quote(query)

        url = f"https://www.google.com/search?q={encoded_query}"

        webbrowser.open(url)

      else:
        speak("What would you like me to search?")

        
    # Google search
    elif command.startswith("search"):

        query = command.replace("search", "", 1).strip()

        search_google(query)

    # Wikipedia search

    elif command.startswith("wikipedia"):

     query = command.replace(
        "wikipedia",
        "",
        1
     ).strip()

     search_wikipedia(query)

    # YouTube search
    elif command.startswith("youtube"):

        query = command.replace("youtube", "", 1).strip()

        search_youtube(query)


    # Name
    elif "your name" in command:

        speak("I am your Python voice assistant.")


    # Exit
    elif (
        "stop" in command
        or "exit" in command
        or "quit" in command
        or "goodbye" in command
    ):

        speak("Goodbye! Have a nice day.")

        return False


    else:

        speak(
            "I don't know that command yet. "
            "You can ask me for the time, date, "
            "Google search, or YouTube search."
        )

    return True


# -----------------------------
# MAIN
# -----------------------------

def main():

    speak(
        "Hello! I am your Python voice assistant. "
        "How can I help you?"
    )

    while True:

        command = listen()

        if command:

            continue_running = process_command(command)

            if not continue_running:
                break
        else:
         speak("Sorry, I don't know that command yet.")

# -----------------------------
# START
# -----------------------------
if __name__ == "__main__":
    main()