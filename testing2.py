import keyboard
from time import sleep

def cum(text):
    print(text)

sleep(1)
keyboard.add_hotkey("num_9", lambda: cum("balls"))

keyboard.wait()