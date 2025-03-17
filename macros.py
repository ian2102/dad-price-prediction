import pyautogui

# all positions are for 1920x1080 resolution

def refresh():
    refresh_button = (1784, 278)
    current_position = pyautogui.position()

    if current_position != refresh_button:
        pyautogui.moveTo(refresh_button[0], refresh_button[1], duration=0.2)

    pyautogui.click()

def screenshot_section():
    image_range = (871, 0, 1276 - 871, 1080)
    screenshot = pyautogui.screenshot(region=image_range)
    return screenshot

def move_to_index(index):
    start_pos = (878, 352)
    y_jump = 65
    pos = (start_pos[0], start_pos[1] + (y_jump * index))
    pyautogui.moveTo(pos[0], pos[1], duration=0.1)

