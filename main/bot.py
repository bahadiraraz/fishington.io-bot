from cv2 import cv2
import mss
import numpy as np
import os
import time
#from pynput.mouse import Button, Controller
from pynput import mouse, keyboard
import random
import pyautogui
import pydirectinput

class Fisher:
    def __init__(self):
        self.stc = mss.mss()

        path = os.path.dirname(os.path.dirname(__file__))
        self.img_path = os.path.join(path, 'img')
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()

        self.bar_top = 0
        self.bar_left = 0
        self.fish_count = 0
        self.fish_limit = 16
        self.throw_count = 1
        self.fish_total_count = 0
        self.keep_fishing = True

    def fish(self):
        while self.keep_fishing:
            if self.close_caught_fish():
                # We caught a fish
                self.fish_count += 1
                self.fish_total_count += 1
                print(f"Fish in Basket: {self.fish_count} / {self.fish_limit}, Total Fish Count: {self.fish_total_count}")
            if self.is_bobber():
                time.sleep(10)
                continue
            if self.fish_count >= self.fish_limit:
                    self.Sell_Fish()
                    continue
            #Reset click
            jitter = random.randint(-25, 25)
            cast_jitter = random.random()
            click_time = .2 + cast_jitter
            pydirectinput.click(800 + jitter,800 + jitter)
            time.sleep(1)
            self.Click_Location(800 + jitter,800 + jitter,click_time)
            print(f"Throwing line: {self.throw_count} (time: {round(click_time, 3)}s)")
            self.throw_count += 1
            time.sleep(11)
            self.Click_Location(800 + jitter,800 + jitter,.5)
            time.sleep(.5)

    def is_bobber(self):
        img = self.Screen_Shot()
        bobber_img = cv2.imread(os.path.join(self.img_path, 'bobber.jpg'), cv2.IMREAD_UNCHANGED)
        result_try = cv2.matchTemplate(img, bobber_img, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result_try)
        trigger = .8
        if max_val > trigger:
            print(f"FISH on SLEEPING! (max: {round(max_val, 3)} / {trigger})")
            return True
        else:
            return False

    def Set_Bobber(self):
        while True:
            pydirectinput.click(800,800)
            time.sleep(.6)
            self.Click_Location(800,800,1)
            print("Throwing line:", self.throw_count)
            self.throw_count += 1
            time.sleep(11)
            pydirectinput.click(800,800)
            time.sleep(.6)
            print("Finding Bobber...")
            img = self.Screen_Shot()
            bobber_img = cv2.imread(os.path.join(self.img_path, 'bobber.jpg'), cv2.IMREAD_UNCHANGED)
            result_try = cv2.matchTemplate(img, bobber_img, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result_try)
            trigger = .8
            if max_val > trigger:
                print(f"Bobber found!! (max: {round(max_val, 3)} / {trigger})")
                new_max = max_loc
                bar_top = new_max[1] - 20
                bar_left = new_max[0]
                return bar_left, bar_top
            else:
                print(f"Bobber not found yet. (max: {round(max_val, 3)} / {trigger})")

    def close_caught_fish(self):
        max_loc, max_val = self.Template_Match("YellowX.jpg", self.Screen_Shot())
        trigger = .8
        if max_val > trigger:
            print(f"Fish found, Pushing Yellow X... (max: {round(max_val, 3)} / {trigger})")
            self.Click_Location(max_loc[0] + 10, max_loc[1] + 10)
            self.Click_Location(max_loc[0] + 5, max_loc[1] + 5)
            # Means we caught a fish
            return True
        return False

    def Sell_Fish(self):

        print("Going to store...")
        self.keyboard.press(keyboard.Key.up)
        time.sleep(8)
        self.keyboard.release(keyboard.Key.up)

        self.keyboard.press(keyboard.Key.space)
        time.sleep(1)
        self.keyboard.release(keyboard.Key.space)

        print("Looking for 'Select all' button...")
        max_loc, max_val = self.Template_Match("SellBox.jpg", self.Screen_Shot())
        trigger = .8
        if max_val > trigger:
            print(f"Button found, Pushing 'Select all' button... (max: {round(max_val, 3)} / {trigger})")
            self.Click_Location(max_loc[0] + 20, max_loc[1] + 30)

            # Look for sell button
            time.sleep(1)
            print("Looking for 'SELL FOR' button...")
            max_loc, max_val = self.Template_Match("SellFor.jpg", self.Screen_Shot())
            trigger = .6
            if max_val > trigger:
                print(f"Button found, Pushing 'Sell FOR' button... (max: {round(max_val, 3)} / {trigger})")
                self.Click_Location(max_loc[0] + 40, max_loc[1] + 10)
                time.sleep(1)
                print("Looking for green 'SELL' button...")
                max_loc, max_val = self.Template_Match("Sell.jpg", self.Screen_Shot())
                trigger = .7
                if max_val > trigger:
                    print(f"Button found, Pushing green 'SELL' button... (max: {round(max_val, 3)} / {trigger})")
                    self.Click_Location(max_loc[0] + 10, max_loc[1] + 10)

                    # Get all the way through we return True for sold something
                    time.sleep(1)
                    max_loc, max_val = self.Template_Match("Sell.jpg", self.Screen_Shot())
                    time.sleep(1)
                    self.fish_count = 0
                else:
                    print(f"Green 'SELL' button not found! (max: {round(max_val, 3)} / {trigger})")
            else:
                print(f"'SELL FOR' button not found! (max: {round(max_val, 3)} / {trigger})")
        else:
            print(f"There are no fish to sell! (max: {round(max_val, 3)} / {trigger})")
        self.Click_Location(200,500)
        time.sleep(1)
        self.Click_Location(100,500)
        # Go back fishing...
        print("Going back...")
        self.keyboard.press(keyboard.Key.down)
        time.sleep(8)
        self.keyboard.release(keyboard.Key.down)
        self.keyboard.press(keyboard.Key.down)
        time.sleep(2)
        self.keyboard.release(keyboard.Key.down)
    
    def Screen_Shot(self, left=0, top=0, width=1920, height=1080):
        stc = mss.mss()
        scr = stc.grab({
            'left': left,
            'top': top,
            'width': width,
            'height': height
        })

        img = np.array(scr)
        img = cv2.cvtColor(img, cv2.IMREAD_COLOR)

        return img

    # Compare to images return max value / location
    def Template_Match(self, needle, haystack):
        sell_box_img = cv2.imread(os.path.join(self.img_path, needle), cv2.IMREAD_UNCHANGED)
        result_try = cv2.matchTemplate(haystack, sell_box_img, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result_try)
        return (max_loc, max_val)

    def Click_Location(self, x, y, wait=0):
        pydirectinput.moveTo(x, y)
        pydirectinput.mouseDown()
        time.sleep(wait)
        pydirectinput.mouseUp()
        #self.mouse.position = (x, y)

    def start_fresh(self):
        time.sleep(5)
        self.keyboard.press(keyboard.Key.ctrl)
        self.keyboard.press('r')
        time.sleep(1)
        self.keyboard.release(keyboard.Key.ctrl)
        self.keyboard.release('r')
        time.sleep(1)
        self.keyboard.press(keyboard.Key.enter) 
        self.keyboard.release(keyboard.Key.enter)

# Test our classes and functions
if __name__ == "__main__":
    fisher = Fisher()
    time.sleep(5)
    #fisher.Set_Bobber()
    fisher.Sell_Fish()
    #fisher.close_caught_fish() 
    #fisher.start_fresh()