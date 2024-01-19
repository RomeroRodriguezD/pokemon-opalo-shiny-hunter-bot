import cv2
import pyautogui
import keyboard as kb
import time
import numpy as np


battle_image = './ps_opalo.png'
battle_pattern = cv2.imread(battle_image, cv2.IMREAD_GRAYSCALE)

shining_not = './shiny_opalo.png'
shining_not_catched = cv2.imread(shining_not, cv2.IMREAD_GRAYSCALE)

"""
This will only be used for Pokemon Z when more testing its done.

shining_own = './shining_you_have.png'
shining_owned = cv2.imread(shining_own, cv2.IMREAD_GRAYSCALE)"""

def stop_everything():
    time.sleep(1)

    stop = kb.is_pressed('space')
    return stop

def walking_horizontal():
    pyautogui.keyDown('left')
    time.sleep(0.3)
    pyautogui.keyUp('left')
    pyautogui.keyDown('right')
    time.sleep(0.3)
    pyautogui.keyUp('right')


def fight():
    # battle if not shiny
    pyautogui.keyDown('c')
    pyautogui.keyUp('c')
    time.sleep(0.2)
    pyautogui.keyDown('c')
    pyautogui.keyUp('c')

    time.sleep(1.5)
    pyautogui.keyDown('c')
    pyautogui.keyUp('c')

    time.sleep(0.5)
    pyautogui.keyDown('c')
    pyautogui.keyUp('c')

    time.sleep(0.5)
    pyautogui.keyDown('c')
    pyautogui.keyUp('c')

    time.sleep(0.5)
    pyautogui.keyDown('c')
    pyautogui.keyUp('c')

    time.sleep(1)

    foe_still_alive()


def foe_still_alive():
    screen_ps = pyautogui.screenshot()
    screen_ps = np.array(screen_ps)

    screen_ps_to_cv = cv2.cvtColor(screen_ps, cv2.COLOR_RGB2GRAY)
    ps_found = cv2.matchTemplate(screen_ps_to_cv, battle_pattern, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(ps_found)

    # Threshold to determine if HP bar of the enemy is still there.
    umbral = 0.9

    if max_val >= umbral:
        fight()


def escape_battle():
    # Escape battle if not a shiny appeared
    pyautogui.keyDown('c')
    pyautogui.keyUp('c')
    time.sleep(1.8)
    pyautogui.keyDown('down')
    pyautogui.keyUp('down')
    pyautogui.keyDown('right')
    pyautogui.keyUp('right')
    time.sleep(0.5)
    pyautogui.keyDown('c')
    pyautogui.keyUp('c')
    pyautogui.keyDown('c')
    pyautogui.keyUp('c')

    time.sleep(1)


def check_screen(screen_to_cv):
    global battle_count
    # Looks for the PS (HP) letter from health bar
    battle_found = cv2.matchTemplate(screen_to_cv, battle_pattern, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(battle_found)

    # Match threshold
    umbral = 0.9

    if max_val >= umbral:
        battle_count += 1
        print(f"Fight {battle_count} started!")

        # Checks if there's a shiny pokemon there
        is_there_a_shiny = cv2.matchTemplate(screen_to_cv, shining_not_catched, cv2.TM_CCOEFF_NORMED)
        min_val_shiny, max_val_shiny, min_loc_shiny, max_loc_shiny = cv2.minMaxLoc(is_there_a_shiny)
        umbral_shiny = 0.85

        if max_val_shiny >= umbral_shiny:
            print(f'Shiny pokemon appeared at battle {battle_count}!')
            kb.wait('f2')
        # Here you comment or uncomment your desired option
        escape_battle()
        #fight()

### This function was only used while testing threshold.
def shiny_logo_test(screen_to_cv):
    is_there_a_shiny = cv2.matchTemplate(screen_to_cv, shining_not_catched, cv2.TM_CCOEFF_NORMED)
    min_val_shiny, max_val_shiny, min_loc_shiny, max_loc_shiny = cv2.minMaxLoc(is_there_a_shiny)
    umbral_shiny = 0.85

    if max_val_shiny >= umbral_shiny:
        print('Shiny pokemon that you do not own appeared!')
        kb.wait('f2')


if __name__ == "__main__":
    print('Waiting for the order (F2) to start walking.')
    kb.wait('f2')
    battle_count = 0

    while True:
        walking_horizontal()
        time.sleep(3)  # Gives enough time for a battle screen to appear
        # Takes and checks screenshot
        screen = pyautogui.screenshot()
        screen = np.array(screen)

        screen_to_cv = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)

        check_screen(screen_to_cv)