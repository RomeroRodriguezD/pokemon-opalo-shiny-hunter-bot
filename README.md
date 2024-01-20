## Shiny Pokemon Searcher for Pokémon Ópalo ##


This algorithm combines automation with computer vision in order to "farm" shiny pokemon in
Pokémon Ópalo and Pokémon Z (fangames owned by EricLostie) without doing nothing but waiting for a shiny summon.

**The idea**

The premise is pretty simple: Make your character move and roam through tall grass, meeting pokemon until
a shiny one appears. This implies many points:

1-The character should be able to move in regular patterns, even after a battle, since it should not go
outside of the tall grass.

2-The program should be able to check and determine whether its in a battle or not.

3-If its a battle, the program should be able to determine if the character met a shiny pokemon or it didn't, and behave
accordingly.

4-The program should iterate "endlessly" after all this process, without getting stuck.

5-You should be able to determine when the character starts to be "piloted".

6-Last but not least: The time calculations are done assuming you're setting turbo speed. If not, they should be probably doubled or tripled.

### Main modules ###

We'll need OpenCV, PyAutoGui, Keyboard, Numpy and the in-built Time module.


```python
import cv2
import pyautogui
import keyboard as kb
import time
import numpy as np

```

## Setting some pre-requisites ##

Since it will be using visual pattern matching, we'll need to have them captured on files in order to make it work.
Those patterns should be some graphic element that <b>should only be found in our desired context to make it impossible to misinterpret.</b>

So, for Pokémon Ópalo we use two perfect matches:

1-The "PS" (HP in English games) letters from an opposing Pokemon health bar, that appears immediately when meeting a wild Pokemon.
This will tell to the algorithm "Hey, we are in a battle!".

2-The "Star sign" characteristic of a Shiny Pokemon, that appears close to the health bar.

<b>Those images should be screen captures from the game itself, at the specific resolution we want to play.  Size matters.</b> 

This ones are based on a full-screen game played at 1980x1080 resolution:

```python
battle_image = './ps_opalo.png'
battle_pattern = cv2.imread(battle_image, cv2.IMREAD_GRAYSCALE)

shining_not = './shiny_opalo.png'
shining_not_catched = cv2.imread(shining_not, cv2.IMREAD_GRAYSCALE)

```

Those are the images before any process:

PS letters

![ps_opalo](https://github.com/RomeroRodriguezD/pokemon-palo-shiny-hunter-bot/assets/105886661/11dc72c6-a831-47c4-92f8-f6205a4bc98f)

Shiny star

![shiny_opalo](https://github.com/RomeroRodriguezD/pokemon-palo-shiny-hunter-bot/assets/105886661/ba720b10-230d-41cc-bd4c-2a5d8b9be3f9)

However, the program works at gray scale. That's because two reasons:

1-Color gives us 0 relevant information for this task. In fact, it would only make the pattern matching harder.

2-Working with gray scales is faster than colorized spectrums.

## Defining the key functions ##

Once we've got the base images, let's define the needed functions.

First of all, we need the character to move. I've chosen to do it horizontally, just personal preference.

```python
def walking_horizontal():
    pyautogui.keyDown('left')
    time.sleep(0.3)
    pyautogui.keyUp('left')
    pyautogui.keyDown('right')
    time.sleep(0.3)
    pyautogui.keyUp('right')
```

Assume we met a Pokemon we don't want to fight. We'll need a way to get out of the situation, <b>we can chose to
either escape the battle</b>:

```python
def escape_battle():
    # Escapes battle if not a shiny appeared
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
```
Or <b>fight back</b> with our first attack (top-left corner), until the enemy is knocked out, which will also need
a recursive function to keep attacking in case our enemy is still alive. Notice that this option will eventually leave us without PP or dead, breaking the actions chain purpose:

```python
def fight():
    # Fight if not shiny
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
```

Now, we'll need something to check what's already happening in the screen, so all our previous functions can be organized to work together. 
It will also keep track of the battle count, so we know how many pokemon the bot met, and when the shiny pokemon appeared

```python
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
```

<h3><b>Wrapping it up:</b></h3>
We'll be waiting for an "F2" press to start the bot. It will wait endlessly for another "F2" press if it finds a shiny.

```python
if __name__ == "__main__":
    print('Waiting for the order (F2) to start walking.')
    kb.wait('f2')
    battle_count = 0
    
    while True:
        walking_horizontal()
        time.sleep(3) # Gives enough time for a battle screen to appear
        # Takes and checks screenshot
        screen = pyautogui.screenshot()
        screen = np.array(screen)
    
        screen_to_cv = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
    
        check_screen(screen_to_cv)
```
<h3><b>Output sample</b></h3>

![image](https://github.com/RomeroRodriguezD/pokemon-palo-shiny-hunter-bot/assets/105886661/a27f9ade-6387-49dc-826c-e50b4fecce15)

<h3><b>Final thoughts & Sidenotes</b></h3>

-Pattern matching is a powerful tool when we are looking for non-changing, distinguishable visual elements, letting us automate
many things. This game is just an example.

-While this may also work with Pokémon Z (and perhaps other Lostieverse fangames), and it does if you don't have the pokemon yet, there's still one case I did not test and may not work: shiny wild pokemon
that you already have, whom have a different shiny logo.

-The exact same technique could be used for, for example, look for a rare pokemon with a very low chance to appear, with just a few code lines changed and using the desired pokemon matching image.
