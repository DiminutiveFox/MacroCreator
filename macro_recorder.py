from pynput import keyboard, mouse
import pandas as pd
import sys, os
import time

class MyException(Exception):
    """Class for stopping the key registration thread"""
    pass

class TriggerException(Exception):
    """Class for registering trigger occurrence"""
    pass

class KeyRecorder:
    """Class for macro creation"""
    def __init__(self):
        self.__mouse_listener = mouse.Listener(on_click=self.__on_click_record_key)
        self.__keyboard_listener = keyboard.Listener(on_press=self.__on_press_record_key)
        self.__key_db = pd.DataFrame(columns=['Device', 'Key', 'X', 'Y'])
        sys.tracebacklimit = 0

    def __on_press_record_key(self, key):
        if key == keyboard.Key.esc:
            raise MyException
        if str(key) == "'`'":
            self.__key_db.loc[len(self.__key_db.index), 'Device':'Y'] = ['mouse', 'Button.left', 'x', 'y']
        else:
            self.__key_db.loc[len(self.__key_db.index), 'Device':'Key'] = ['keyboard', str(key)]

    def __on_click_record_key(self, x, y, button, pressed):
        if pressed:
            self.__key_db.loc[len(self.__key_db.index), 'Device':'Y'] = ['mouse', str(button), x, y]

    def record_macro(self, macro_filename="macro.csv", dir_path="macros\\"):
        """Creates a .csv file with all mouse's and keyboard's typings. Press esc to stop"""
        if not macro_filename.endswith('.csv'):
            print("WRONG FILENAME!")
            return
        self.__mouse_listener.start()
        self.__keyboard_listener.start()
        try:
            self.__keyboard_listener.join()
        except MyException:
            self.__mouse_listener.stop()
            self.__keyboard_listener.stop()
            self.__key_db.to_csv(dir_path + macro_filename)
            os.system('cls')
            return


class KeyRegister:
    """Class for single key registration"""
    def __init__(self):
        self.__mouse_listener = mouse.Listener(on_click=self.__on_click_register_key)
        self.__keyboard_listener = keyboard.Listener(on_press=self.__on_press_register_key)
        sys.tracebacklimit = 0
        self.hotkey = ""
        self.trigger = ""
        self.listening_trigger = False

    def __on_press_register_key(self, key):
        if key == keyboard.Key.esc:
            raise MyException
        else:
            if not self.listening_trigger:
                self.hotkey = str(key)
            else:
                if str(key).replace("'", "") == self.trigger.replace("'", ""):
                    raise TriggerException
                else:
                    print(f"Key pressed: {key}")

    def __on_click_register_key(self, x, y, button, pressed):
        if not self.listening_trigger:
            self.hotkey = str(button)
        else:
            if str(button).replace("'", "") == self.trigger:
                self.__keyboard_listener.stop()
                raise TriggerException
            else:
                print(f"Key pressed: {button}")

    def register_key(self):
        """Registers mouse or keyboard key and returns it. Press esc to stop and register"""
        time.sleep(0.1)
        self.__mouse_listener.start()
        self.__keyboard_listener.start()
        try:
            self.__keyboard_listener.join()
        except MyException:
            self.__keyboard_listener.stop()
            self.__mouse_listener.stop()
            return self.hotkey

    def listen_for_trigger(self, key_trigger):
        time.sleep(0.1)
        self.trigger = str(key_trigger)
        self.listening_trigger = True
        self.__mouse_listener.start()
        self.__keyboard_listener.start()
        try:
            self.__keyboard_listener.join()
            self.__mouse_listener.join()
        except MyException:
            self.__keyboard_listener.stop()
            self.__mouse_listener.stop()
            return False
        except TriggerException:
            self.__keyboard_listener.stop()
            self.__mouse_listener.stop()
            return True
