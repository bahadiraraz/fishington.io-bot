from cv2 import cv2
import mss
import numpy as np
import os
import time
#from pynput.mouse import Button, Controller
from pynput import mouse, keyboard

class Fisher:
    def __init__(self):
        self.stc = mss.mss()

        path = os.path.dirname(os.path.dirname(__file__))
        self.img_path = os.path.join(path, 'img')
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()

        self.bar_top = 0
        self.bar_left = 0

    def Set_Bobber(self):
        while True:
            self.Click_Location(800,800,2)
            print("finding Bobber")
            img = self.Screen_Shot()
            bobber_img = cv2.imread(os.path.join(self.img_path, 'bobber.jpg'), cv2.IMREAD_UNCHANGED)
            result_try = cv2.matchTemplate(img, bobber_img, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result_try)
            if max_val > .9:
                print("Found it waiting... 5 don't Click!")
                new_max = max_loc
                time.sleep(5)
                img = self.Screen_Shot()
                bobber_img = cv2.imread(os.path.join(self.img_path, 'bobber.jpg'), cv2.IMREAD_UNCHANGED)
                result_try = cv2.matchTemplate(img, bobber_img, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result_try)
                if max_val > .9:
                    print("Updating max")
                    new_max = max_loc
                bar_top = new_max[1]
                bar_left = new_max[0]
                return bar_left, bar_top

            print(f"Current Max: {max_val} sleeping")
            time.sleep(7)
            self.Click_Location(800,800,.5)
            time.sleep(.5)


    def Sell_Fish(self):

        # Get to store if we are not there...
        self.keyboard.press(keyboard.Key.up)
        time.sleep(1)
        self.keyboard.release(keyboard.Key.up)

        self.keyboard.press(keyboard.Key.space)
        time.sleep(1)
        self.keyboard.release(keyboard.Key.space)

        max_loc, max_val = self.Template_Match("SellBox.jpg", self.Screen_Shot())
        if max_val > .9:
            print("We got fish to sell!")
            self.Click_Location(max_loc[0] + 10, max_loc[1] + 10)

            # Look for sell button
            time.sleep(1)
            print("Looking to for sell")
            max_loc, max_val = self.Template_Match("SellFor.jpg", self.Screen_Shot())
            if max_val > .9:
                print("Pushing Sell") 
                self.Click_Location(max_loc[0] + 10, max_loc[1] + 10)

                time.sleep(1)
                print("Looking to for sell Green")
                max_loc, max_val = self.Template_Match("Sell.jpg", self.Screen_Shot())
                if max_val > .9:
                    print("Pushing Sell Green")
                    self.Click_Location(max_loc[0] + 10, max_loc[1] + 10)

                    # Get all the way through we return True for sold something
                    time.sleep(1)
                    return True
        self.Click_Location(200,200)
        self.Click_Location(200,200)
        return False
    
    def Screen_Shot(self, left=0, top=0, width=1920, height=1080):
        scr = self.stc.grab({
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

    def Click_Location(self, x, y, pause=0):
        self.mouse.position = (x, y)
        self.mouse.press(mouse.Button.left)
        time.sleep(pause)
        self.mouse.release(mouse.Button.left)


# Test our classes and functions
if __name__ == "__main__":
    fisher = Fisher()
    time.sleep(5)
    while fisher.Sell_Fish():
        print("Selling Fish")