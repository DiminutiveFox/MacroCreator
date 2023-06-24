import time
import pandas as pd
from pynput import mouse, keyboard
from pynput.keyboard import Key
from pynput.mouse import Button

class MacroReader:
    def __init__(self, hotkey_database_name):
        self.hotkey_database = pd.read_csv(hotkey_database_name)
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()

    def macro_reader(self, key_database_name, object_loc=[0, 0], finder=False, relative=False, pause=0.15, counter=0):

        key_database = pd.read_csv(key_database_name) if relative == False else \
            self.mouse_loc_calc(key_database_name, self.mouse_controller.position if not finder
                                else object_loc)

        first_mouse_click = True
        for n in range(len(key_database.index)):
            time.sleep(pause)
            print(key_database.loc[n, 'Key'])
            # If instance is a mouse type, then do something with the mouse
            if key_database.loc[n, 'Device'] == 'mouse':
                # If there are 'x' and 'y' in Coords columnns, it means that the coordinates are not fixed
                # And we want mouse to go to the location specified in function call - this is meant for
                # performing macro on every object found on the screen and file macro.csv should be modified
                # in order to achieve that
                if key_database.loc[n, 'X'] == 'x' and key_database.loc[n, 'Y'] == 'y':
                    # self.mouse_controller.move(x, y)
                    pass
                else:
                    if finder and first_mouse_click:
                        print(object_loc)
                        position = object_loc
                        first_mouse_click = False
                    else:
                        position = (key_database.loc[n, 'X'], key_database.loc[n, 'Y'])
                    if int(position[0]) < 0 or int(position[1]) < 0:
                        print("Error - mouse position cannot exceed screen resolution")
                    self.mouse_controller.position = position
                if key_database.loc[n, 'Key'] == 'Button.left':
                    self.mouse_controller.press(Button.left)
                    time.sleep(0.1)
                    self.mouse_controller.release(Button.left)
                elif key_database.loc[n, 'Key'] == 'Button.right':
                    self.mouse_controller.press(Button.right)
                    time.sleep(0.1)
                    self.mouse_controller.release(Button.right)

                else:
                    self.mouse_controller.press(Button.middle)
                    time.sleep(0.1)
                    self.mouse_controller.release(Button.middle)

            # If instance is of keyboard type, then click sth on keyboard
            if key_database.loc[n, 'Device'] == 'keyboard':
                key = key_database.loc[n, 'Key'].replace("'", "")
                # If we clicked ctrl we assume that we performed a hotkey procedure during macro
                # There is special key for every crtl hotkey in key dictionary and in next elif we look for it
                # Here we just skip this line and click nothing
                if key == 'Key.ctrl_l' or key == 'Key.shift':
                    continue
                # If key is in key dictionary, then perform hotkey eg ctrl+c
                elif key in self.hotkey_database['Special Key'].values:
                    index = self.hotkey_database[self.hotkey_database == key].stack().index.tolist()[0][0]
                    with self.keyboard_controller.pressed(keyboard.Key.ctrl):
                        self.keyboard_controller.press(self.hotkey_database.loc[index, 'Key'])
                # If key is just an ordinary key eg 'k', then click k
                elif len(key) > 1:
                    self.keyboard_controller.press(eval(key))
                    self.keyboard_controller.release(eval(key))
                elif key == '$':
                    self.keyboard_controller.type(key_database[n, 'X'])
                elif key == '#':
                    self.keyboard_controller.type(str(counter))
                else:
                    self.keyboard_controller.press(key)
                    self.keyboard_controller.release(key)

    def mouse_loc_calc(self, key_database_name, click_loc):
        key_database = pd.read_csv(key_database_name)
        previous_click_loc = []
        mouse_clicks = 0
        for n in range(len(key_database.index)):
            if key_database.loc[n, 'Device'] == 'mouse':
                if mouse_clicks < 1:
                    previous_click_loc = key_database.loc[n, 'X':'Y']
                    key_database.loc[n, 'X':'Y'] = click_loc
                    new_click_loc = key_database.loc[n, 'X':'Y']
                else:
                    relative_loc = [key_database.loc[n, 'X'] - previous_click_loc[0],
                                    key_database.loc[n, 'Y'] - previous_click_loc[1]]
                    previous_click_loc = key_database.loc[n, 'X':'Y']
                    key_database.loc[n, 'X':'Y'] = [new_click_loc[0] + relative_loc[0],
                                                    new_click_loc[1] + relative_loc[1]]
                    new_click_loc = key_database.loc[n, 'X':'Y']
                mouse_clicks += 1
        return key_database

#In case file is lost
key_dictionary = [('ctrl', '\\x11', 'q'),
('ctrl', '\\x17', 'w'),
('ctrl', '\\x05', 'e'),
('ctrl', '\\x12', 'r'),
('ctrl', '\\x14', 't'),
('ctrl', '\\x19', 'y'),
('ctrl', '\\x15', 'u'),
('ctrl', '\\t', 'i'),
('ctrl', '\\x0f', 'o'),
('ctrl', '\\x10', 'p'),
('ctrl', '\\x01', 'a'),
('ctrl', '\\x13', 's'),
('ctrl', '\\x04', 'd'),
('ctrl', '\\x06', 'f'),
('ctrl', '\\x07', 'g'),
('ctrl', '\\x08', 'h'),
('ctrl', '\\n', 'j'),
('ctrl', '\\x0b', 'k'),
('ctrl', '\\x0c', 'l'),
('ctrl', '\\x1a', 'z'),
('ctrl', '\\x18', 'x'),
('ctrl', '\\x03', 'c'),
('ctrl', '\\x16', 'v'),
('ctrl', '\\x02', 'b'),
('ctrl', '\\x0e', 'n'),
('ctrl', '\\r', 'm')]