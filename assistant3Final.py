import tkinter as tk
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import threading
import datetime
import webbrowser
import os
import math

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    def run():
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            pass

    threading.Thread(target=run).start()
    status_var.set(text)

wave_lines = []
wave_running = False

def create_wave():
    for i in range(30):
        line = canvas.create_line(0, 0, 0, 0, fill="#00e5ff", width=3)
        wave_lines.append(line)

def animate_wave():
    if not wave_running:
        return

    center_x = 200
    base_y = 260

    for i, line in enumerate(wave_lines):
        x = center_x - 150 + i * 10
        height = 40 * math.sin((i + animate_wave.frame) * 0.3)

        canvas.coords(line,
                      x, base_y - height,
                      x, base_y + height)

    animate_wave.frame += 1
    root.after(50, animate_wave)

animate_wave.frame = 0

def start_wave():
    global wave_running
    wave_running = True
    animate_wave()

def stop_wave():
    global wave_running
    wave_running = False

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_var.set("Listening...")
        start_wave()

        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        user_var.set(command)
        return command.lower()
    except:
        status_var.set("Didn't catch...")
        return "none"
    finally:
        stop_wave()

def main_logic():
    query = listen()

    if "open chrome" in query:
        speak("Opening Google Chrome browser.")
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if os.path.exists(chrome_path):
            os.startfile(chrome_path)
        

    elif "open google" in query:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    elif "open notepad" in query:
        speak("Opening Notepad.")
        os.system("notepad.exe")

    elif "open calculator" in query:
        speak("Opening Calculator.")
        os.system("calc.exe")

    elif "open youtube" in query:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    elif "open settings" in query or "setting" in query:
        speak("Opening your system settings.")
        os.system("start ms-settings:")
    
    elif "open whatsapp" in query:
        speak("Opening WhatsApp.")
        os.system("start whatsapp:")

    elif "exit" in query:
        speak("Shutting down. Have a great day!")
        root.destroy()

    elif "open steam" in query:
        speak("Opening Steam. Get ready to play.")
        steam_path = r"C:\Program Files (x86)\Steam\steam.exe"
        os.startfile(steam_path)

    elif "open vs code" in query:
        speak("Opening Visual Studio Code. Happy coding!")
        vscode_path = r"C:\Users\abhay\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        os.startfile(vscode_path)
    else:
        speak("I didn't understand")

def start():
    threading.Thread(target=main_logic).start()


root = tk.Tk()
root.title("AURA AI")
root.geometry("400x600")
root.configure(bg="black")
root.resizable(False, False)

canvas = tk.Canvas(root, width=400, height=600, bg="black", highlightthickness=0)
canvas.pack()

try:
    img = Image.open("aura.jpg")
    img = img.resize((180, 220))
    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(200, 260, image=img_tk)
    canvas.img = img_tk
except:
    print("Image missing")

canvas.create_text(200, 80, text="AURA AI",
                   fill="#00e5ff", font=("Arial", 26, "bold"))


status_var = tk.StringVar(value="Initializing...")
status_label = tk.Label(root, textvariable=status_var,
                        fg="white", bg="black",
                        font=("Arial", 12))
canvas.create_window(200, 120, window=status_label)


user_var = tk.StringVar()
user_label = tk.Label(root, textvariable=user_var,
                      fg="#aaaaaa", bg="black",
                      font=("Arial", 10))
canvas.create_window(200, 150, window=user_label)


create_wave()


mic_btn = tk.Button(root, text="🎤", font=("Arial", 20),
                    bg="#00e5ff", fg="black",
                    activebackground="#00bcd4",
                    relief="flat", command=start)

canvas.create_window(200, 520, window=mic_btn)


def welcome():
    speak("Welcome, I am Aura. How can I help you?")

root.after(1000, welcome)

root.mainloop()