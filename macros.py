import pyautogui

# all positions are for 1920x1080 resolution

def refresh():
    refresh_button = (1784, 278)
    current_position = pyautogui.position()

    if current_position != refresh_button:
        pyautogui.moveTo(refresh_button[0], refresh_button[1], duration=0.2)

    pyautogui.click()

