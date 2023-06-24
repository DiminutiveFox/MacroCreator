import pandas as pd
import customtkinter
import time
import macro_executor
import object_finder
import macro_recorder
from idlelib.tooltip import Hovertip
import os


class PopUpWindow(customtkinter.CTkToplevel):
    """Message box with user acknowledge"""
    def __init__(self, master, text, title="Warning!"):
        super().__init__(master)
        self.info_text = text
        self.title(title)
        self.attributes('-topmost', True)
        self.title = customtkinter.CTkLabel(self, text=self.info_text, fg_color="transparent", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(0, 30), sticky="ew")
        self.close = False
        self.button = customtkinter.CTkButton(self, text="START", command=self.close_self, width=50, height=20)
        self.button.grid(row=0, column=0, padx=10, pady=(50, 10), sticky="ew")
        self.wait_window(self)

    def close_self(self):
        self.destroy()
        self.update()

class ObjectFinderFrame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.bg_color = "#96caf3"
        self.widget_color = "#6699cc"
        self.disabled_widget_color = "gray80"
        self.run_button_color = "green"
        self.left_offset = 10
        self.right_offset = 10
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.master = master
        self.width = (master.width - 30)/2
        self.height = master.height - 20
        self.configure(width=self.width, height=self.height, fg_color=self.bg_color)

        # Atributes
        self.images_list = self.master.list_files("\\images", ".png")
        self.locations_list = self.master.list_files("\\locations", ".csv")
        self.active_objects =  3*["---"]
        self.variable = customtkinter.StringVar(value="")
        self.loc_visible = False

        # Area of images specification
        self.object_list_label = customtkinter.CTkLabel(self.master, text="Pick objects that you want to find:",
                                                        fg_color=self.bg_color, bg_color=self.bg_color,
                                                        width=self.width / 3, height=self.height / 18)
        self.object_list_label.grid(row=0, column=1, padx=(self.left_offset, 0),
                                    pady=(0, self.height - 0.5 * self.height / 6), sticky="w")

        self.option_menu_object1 = customtkinter.CTkOptionMenu(self.master, values=self.images_list,
                                                               width=2 * self.width / 3,
                                                               height=self.height / 18, bg_color=self.bg_color,
                                                               command=self.__optionmenu1_callback,
                                                               fg_color=self.widget_color)
        self.option_menu_object1.grid(row=0, column=1, padx=(self.left_offset, 0),
                                      pady=(0, self.height - 1.2 * self.height / 6), sticky="w")
        self.option_menu_object2 = customtkinter.CTkOptionMenu(master, values=self.images_list,
                                                               width=2 * self.width / 3,
                                                               height=self.height / 18, bg_color=self.bg_color,
                                                               command=self.__optionmenu2_callback,
                                                               fg_color=self.widget_color)
        self.option_menu_object2.grid(row=0, column=1, padx=(self.left_offset, 0),
                                      pady=(0, self.height - 2 * self.height / 6), sticky="w")
        self.option_menu_object3 = customtkinter.CTkOptionMenu(master, values=self.images_list,
                                                               width=2 * self.width / 3,
                                                               height=self.height / 18, bg_color=self.bg_color,
                                                               command=self.__optionmenu3_callback,
                                                               fg_color=self.widget_color)
        self.option_menu_object3.grid(row=0, column=1, padx=(self.left_offset, 0),
                                      pady=(0, self.height - 2.8 * self.height / 6), sticky="w")
        self.option_menu_object1.set(self.images_list[1] if len(self.images_list) > 1 else self.images_list[0])
        self.active_objects[0]  = self.images_list[1] if len(self.images_list) > 1 else self.images_list[0]

        #Insight buttons
        self.insight_button1 = customtkinter.CTkButton(master, text="Open", width=self.width / 4,
                                                       height=self.height / 18, bg_color=self.bg_color,
                                                       command=self.__insight_callback1, fg_color=self.widget_color)
        self.insight_button1.grid(row=0, column=1, padx=(10+2*self.width / 3,0),
                                  pady=(0, self.height - 1.2 * self.height / 6), sticky="w")
        self.insight_button2 = customtkinter.CTkButton(master, text="Open", width=self.width / 4,
                                                       height=self.height / 18, bg_color=self.bg_color,
                                                       command=self.__insight_callback2, fg_color=self.widget_color)
        self.insight_button2.grid(row=0, column=1, padx=(10 + 2 * self.width / 3, 0),
                                  pady=(0, self.height - 2 * self.height / 6), sticky="w")
        self.insight_button3 = customtkinter.CTkButton(master, text="Open", width=self.width / 4,
                                                       height=self.height / 18, bg_color=self.bg_color,
                                                       command=self.__insight_callback3, fg_color=self.widget_color)
        self.insight_button3.grid(row=0, column=1, padx=(10 + 2 * self.width / 3, 0),
                                  pady=(0, self.height - 2.8 * self.height / 6), sticky="w")

        # Entry - object finder accuracy
        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.accuracy_label = customtkinter.CTkLabel(self.master, text="Accuracy of object finder (0~1):",
                                                    fg_color=self.bg_color, bg_color=self.bg_color,
                                                    width=2 * self.width / 3, height=self.height / 18)
        self.accuracy_label.grid(row=0, column=1, padx=(5, 0), pady=(0, self.height - 3.6 * self.height / 6),
                                 sticky="w")
        self.accuracy_entry = customtkinter.CTkEntry(self.master, width=self.width / 7, height=self.height / 18,
                                                     border_color=self.widget_color, bg_color=self.bg_color,
                                                     validate='key', validatecommand=vcmd)
        self.accuracy_entry.insert(0, 0.5)
        self.accuracy_entry.grid(row=0, column=1, padx=(10 + 3 * self.width / 4, 0),
                                 pady=(0, self.height - 3.6 * self.height / 6),
                                 sticky="w")

        # Button for finding objects
        self.object_finder_label = customtkinter.CTkLabel(self.master, text="Specify the objects' filename:",
                                                     fg_color=self.bg_color, width=self.width / 3,
                                                     height=self.height / 18, bg_color=self.bg_color)
        self.object_finder_label.grid(row=0, column=1, padx=(self.left_offset, 0),
                                 pady=(0, self.height - 4.4 * self.height / 6), sticky="w")
        self.object_filename_entry = customtkinter.CTkEntry(self.master, height=self.height / 18,
                                                            bg_color=self.bg_color, border_color=self.widget_color,
                                                            width=(self.width - 30) / 2 + 45)
        self.object_filename_entry.grid(row=0, column=1, padx=(self.left_offset, 0),
                                       pady=(0, self.height - 5 * self.height / 6), sticky="w")
        self.object_finder_button = customtkinter.CTkButton(master, text="Find Objects", width=self.width / 4,
                                                            height=self.height / 18, bg_color=self.bg_color,
                                                            command=self.__find_objects_callback,
                                                            fg_color=self.widget_color)
        self.object_finder_button.grid(row=0, column=1,
                                        padx=(50 + (self.width - (self.left_offset + self.right_offset)) / 2, 0),
                                        pady=(0, self.height - 5 * self.height / 6), sticky="w")

        # Checkbox - working with object finder
        self.object_finder_checkbox = customtkinter.CTkCheckBox(self.master, text="Working with object finder",
                                                                width=50,
                                                                command=self.__object_finder_checkbox_callback,
                                                                onvalue=1, offvalue=0, bg_color=self.bg_color,
                                                                height=self.height / 18, hover_color="gray20")
        self.object_finder_checkbox.grid(row=0, column=1, padx=(self.left_offset, 0), pady=(0, 0),
                                         sticky="w")

        # Option menu - picking the file with objects' locations
        self.objects_loc_label = customtkinter.CTkLabel(self.master, text="Pick the list of objects:",
                                                        fg_color=self.bg_color, bg_color=self.bg_color,
                                                        width=self.width / 3, height=self.height / 18)
        self.objects_loc_label.grid(row=0, column=1, padx=(self.left_offset, 0),
                                    pady=(self.height / 6, 0), sticky="w")
        self.option_menu_objects_loc = customtkinter.CTkOptionMenu(self.master, values=self.locations_list,
                                                                   width=2 * self.width / 3, state="disabled",
                                                                   height=self.height / 18,
                                                                   command=self.show_start_button,
                                                                   fg_color=self.disabled_widget_color,
                                                                   bg_color=self.bg_color)

        self.option_menu_objects_loc.grid(row=0, column=1, padx=(self.left_offset, 0),
                                          pady=(1.6 * self.height / 6, 0), sticky="w")
        self.insight_button4 = customtkinter.CTkButton(self.master, text="Open", width=self.width / 4, state="disabled",
                                                       height=self.height / 18, bg_color=self.bg_color,
                                                       command=self.__insight_callback4,
                                                       fg_color=self.disabled_widget_color)
        self.insight_button4.grid(row=0, column=1, padx=(10 + 2 * self.width / 3, 0),
                                  pady=(1.6 * self.height / 6, 0), sticky="w")


        # Button - start macro with object finder
        self.start_macro_button = customtkinter.CTkButton(self.master, text="Start", width=self.width / 2,
                                                          height=self.height / 12, bg_color=self.bg_color,
                                                          command=self.__start_macro_callback,
                                                          fg_color=self.run_button_color, state="disabled")
        self.start_macro_button.grid(row=0, column=1,
                                     padx=(self.left_offset + self.width / 4, 0),
                                     pady=(5 * self.height / 6, 0), sticky="w")

        # Tooltips - Option menus
        self.option_menu1_tooltip = Hovertip(self.option_menu_object1,
                                             text="Menu for picking images. Images are stored \n"
                                                  "in a 'images' folder. Create a screenshot and \n"
                                                  "place it in this folder to be able to pick it here")
        self.option_menu2_tooltip = Hovertip(self.option_menu_object2,
                                            text="Menu for picking images. Images are stored \n"
                                                 "in a 'images' folder. Create a screenshot and \n"
                                                 "place it in this folder to be able to pick it here")
        self.option_menu3_tooltip = Hovertip(self.option_menu_object3,
                                             text="Menu for picking images. Images are stored \n"
                                                  "in a 'images' folder. Create a screenshot and \n"
                                                  "place it in this folder to be able to pick it here")
        # Tooltips - Open Buttons
        self.insight_button1_tooltip = Hovertip(self.insight_button1,
                                                text="Opens the file specified in the drop down menu on the left")
        self.insight_button2_tooltip = Hovertip(self.insight_button2,
                                                text="Opens the file specified in the drop down menu on the left")
        self.insight_button3_tooltip = Hovertip(self.insight_button3,
                                                text="Opens the file specified in the drop down menu on the left")
        self.insight_button4_tooltip = Hovertip(self.insight_button4,
                                                text="Opens the file specified in the drop down menu on the left.\n"
                                                     "Enabled, when 'Working with object finder' checkbox is clicked.")
        # Tooltip - Accuracy entry
        self.accuracy_entry_tooltip = Hovertip(self.accuracy_entry,
                                                      text="Specify the accuracy of the object finder. Value has to be \n"
                                                           "between 0 and 0.99. It cannot end with a decimal point eg. '0.' -\n"
                                                           "then the default value is used")
        # Tooltip - Filename Entry
        self.object_filename_entry_tooltip = Hovertip(self.object_filename_entry,
                                                text="Specify the name of the file where the objects' locations will be\n"
                                                     "stored. It needs to end with the '.csv' extension eg. 'loc.csv'.")

        # Tooltip - Object Finder Button
        self.object_finder_button_tooltip = Hovertip(self.object_finder_button,
                                                      text="Objects' locations (X, Y) will be stored in the 'locations' directory.\n"
                                                           "If filename is not specified, default filename will be used. Also the \n"
                                                           "'.png' file with found objects is generated.")
        # Tooltip - Working with object finder checkbox
        self.object_finder_checkbox_tooltip = Hovertip(self.object_finder_checkbox,
                                                       text="Enables macro execution with object finder.")

        # Tooltips - Option menus
        self.option_menu_objects_loc_tooltip = Hovertip(self.option_menu_objects_loc,
                                                        text="Menu for picking file with objects' locations. It is enabled,\n"
                                                             "when 'Working with object finder' checkbox is clicked.\n"
                                                             "If correct file is picked, the start button is enabled")
        # Tooltip - Object Finder Button
        self.start_macro_button_tooltip = Hovertip(self.start_macro_button,
                                                     text="Macro is executed for every object found on the screen - first mouse click coordinate\n"
                                                          "in macro file is replaced with the object location - the rest of the macro stays the same\n"
                                                          "'Working with offset' checkbox is also applied here")

    # Callback - start macro
    def __start_macro_callback(self):
        text = "Macro is about to start - \nclose all unnecessary windows."
        pop_up_window = PopUpWindow(self, text)
        self.master.run_macro_for_objects()

    # Callbacks - open file buttons
    def __insight_callback1(self):
        try:
            path = str(os.path.dirname(os.path.abspath(__file__))) + "\\images\\" + self.option_menu_object1.get()
            os.system(path)
        except Exception as E:
            print(E)
    def __insight_callback2(self):
        try:
            path = str(os.path.dirname(os.path.abspath(__file__))) + "\\images\\" + self.option_menu_object2.get()
            os.system(path)
        except Exception as E:
            print(E)
    def __insight_callback3(self):
        try:
            path = str(os.path.dirname(os.path.abspath(__file__))) + "\\images\\" + self.option_menu_object3.get()
            os.system(path)
        except Exception as E:
            print(E)

    def __insight_callback4(self):
        try:
            path = str(os.path.dirname(os.path.abspath(__file__))) + "\\locations\\" + \
                   self.option_menu_objects_loc.get().replace(".csv", ".png")
            os.system(path)
        except Exception as E:
            print(E)

    # Callback - find objects button
    def __find_objects_callback(self):
        self.master.minimize_self()
        time.sleep(0.5)
        objects_names = list(filter(lambda a: a != "---", self.active_objects))
        if len(objects_names) >= 1:
            object_finder.find_objects(object_finder.take_screenshot(), objects_names,
                                       float(self.accuracy_entry.get()) if len(self.accuracy_entry.get()) > 2 else 0.6,
                                       str(self.object_filename_entry.get()) if str(
                                           self.object_filename_entry.get()) != '' else "locs.csv")
        else:
            print("No object was choosen!")
        self.update_optionmenus()
        self.master.maximize_self()

    # Callbacks - option menus for image picking
    def __optionmenu1_callback(self, value):
        self.active_objects[0] = value
        print(self.active_objects)
    def __optionmenu2_callback(self, value):
        self.active_objects[1] = value
        print(self.active_objects)
    def __optionmenu3_callback(self, value):
        self.active_objects[2] = value
        print(self.active_objects)

    # Function - enabling the option menu for objects' locations pick
    def show_objects_loc_list(self, visible):
        self.option_menu_objects_loc.configure(state="normal" if visible else "disabled",
                                               fg_color=self.widget_color if visible else self.disabled_widget_color)
        self.insight_button4.configure(state="normal" if visible else "disabled",
                                       fg_color=self.widget_color if visible else self.disabled_widget_color)

    #Callback - object finder checkbox
    def __object_finder_checkbox_callback(self):
        self.master.macro_frame.run_macro_button.configure(state="disabled" if (self.object_finder_checkbox.get() or
                                                                                self.master.macro_frame.offset_macro_checkbox.get()) else "normal")

        self.master.finder = self.object_finder_checkbox.get()
        self.show_objects_loc_list(self.object_finder_checkbox.get())

    # Function - enabling the start button with objects' locations
    def show_start_button(self, value):
        if self.master.finder and self.option_menu_objects_loc.get() != "---":
            self.master.objects = pd.read_csv("locations\\" + value, index_col=0)
            self.start_macro_button.configure(state='normal')
        else:
            self.start_macro_button.configure(state='disabled')

    # Function - used when we generate new object list for updating option menus
    def update_optionmenus(self):
        self.images_list = self.master.list_files("\\images", ".png")
        self.locations_list = self.master.list_files("\\locations", ".csv")
        self.option_menu_object1.configure(values=self.images_list)
        self.option_menu_object2.configure(values=self.images_list)
        self.option_menu_object3.configure(values=self.images_list)
        self.option_menu_objects_loc.configure(values=self.locations_list)

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        """Used for validating user's input in entry"""
        if value_if_allowed:
            try:
                float(value_if_allowed)
                if len(value_if_allowed) < 5:
                    return True
                else:
                    return False
            except ValueError:
                return False
        elif len(value_if_allowed) == 0:
            return True
        else:
            return False

class MacroFrame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)

        #Configuration
        self.width = (master.width - 30)/2
        self.height = master.height-20
        self.bg_color = "#96caf3"
        self.widget_color = "#6699cc"
        self.run_button_color = "green"
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.master = master
        self.configure(width=self.width, height=self.height, fg_color=self.bg_color)

        #Atributes
        self.macros_list = self.master.list_files("\\macros", ".csv")
        self.hotkey = "Button.middle"
        self.offset = False
        self.left_offset = 20
        self.right_offset = 10

        #Macro classes
        self.macro_reader = macro_executor.MacroReader("key_dictionary.csv")

        # Button for macro generation
        self.filename_label = customtkinter.CTkLabel(self.master, text="Specify name of the macro file:",
                                                     fg_color=self.bg_color, width=self.width / 3,
                                                     height=self.height / 18, bg_color=self.bg_color)
        self.filename_label.grid(row=0, column=0, padx=(self.left_offset, 0),
                                 pady=(0, self.height - 0.6 * self.height / 6), sticky="w")
        self.macro_filename_entry = customtkinter.CTkEntry(self.master, height=self.height / 18,
                                                           border_color=self.widget_color,
                                                           width=(self.width - 30) / 2 + 30, bg_color=self.bg_color)
        self.macro_filename_entry.grid(row=0, column=0, padx=(self.left_offset, 0),
                                       pady=(0, self.height - 1.2 * self.height / 6), sticky="w")
        self.generate_macro_button = customtkinter.CTkButton(self.master, text="Generate Macro", width=self.width / 4,
                                                             height=self.height / 18, fg_color=self.widget_color,
                                                             command=self.__generate_macro_callback,
                                                             bg_color=self.bg_color)
        self.generate_macro_button.grid(row=0, column=0,
                                        padx=(50 + (self.width - (self.left_offset + self.right_offset)) / 2, 0),
                                        pady=(0, self.height - 1.2 * self.height / 6), sticky="w")

        # Three option menus of macros for user to choose from
        self.option_menu_label = customtkinter.CTkLabel(self.master, text="Pick macros that you want to run:",
                                                        width=self.width / 3,
                                                        height=self.height / 18, bg_color=self.bg_color)
        self.option_menu_label.grid(row=0, column=0, padx=(self.left_offset, 0),
                                    pady=(0, self.height - 2 * self.height / 6), sticky="w")
        self.option_menu_macro1 = customtkinter.CTkOptionMenu(self.master, values=self.macros_list,
                                                              width=2 * self.width / 3,
                                                              height=self.height / 18, bg_color=self.bg_color,
                                                              command=self.__optionmenu1_callback,
                                                              fg_color=self.widget_color)
        self.option_menu_macro1.grid(row=0, column=0, padx=20, pady=(0, self.height - 2.6 * self.height / 6),
                                     sticky="w")
        self.option_menu_macro2 = customtkinter.CTkOptionMenu(self.master, values=self.macros_list,
                                                              width=2 * self.width / 3,
                                                              height=self.height / 18, bg_color=self.bg_color,
                                                              command=self.__optionmenu2_callback,
                                                              fg_color=self.widget_color)
        self.option_menu_macro2.grid(row=0, column=0, padx=20, pady=(0, self.height - 3.4 * self.height / 6),
                                     sticky="w")
        self.option_menu_macro3 = customtkinter.CTkOptionMenu(self.master, values=self.macros_list,
                                                              width=2 * self.width / 3,
                                                              height=self.height / 18, bg_color=self.bg_color,
                                                              command=self.__optionmenu3_callback,
                                                              fg_color=self.widget_color)
        self.option_menu_macro3.grid(row=0, column=0, padx=20, pady=(0, self.height - 4.2 * self.height / 6),
                                     sticky="w")
        self.option_menu_macro1.set(self.macros_list[1] if len(self.macros_list) > 1 else self.macros_list[0])
        self.master.active_macros[0] = self.option_menu_macro1.get()

        # Insight buttons
        self.insight_button1 = customtkinter.CTkButton(self.master, text="Open", width=self.width / 4,
                                                       height=self.height / 18, bg_color=self.bg_color,
                                                       command=self.__insight_callback1, fg_color=self.widget_color)
        self.insight_button1.grid(row=0, column=0, padx=(20 + 2 * self.width / 3, 0),
                                  pady=(0, self.height - 2.6 * self.height / 6), sticky="w")
        self.insight_button2 = customtkinter.CTkButton(self.master, text="Open", width=self.width / 4,
                                                       height=self.height / 18, bg_color=self.bg_color,
                                                       command=self.__insight_callback2, fg_color=self.widget_color)
        self.insight_button2.grid(row=0, column=0, padx=(20 + 2 * self.width / 3, 0),
                                  pady=(0, self.height - 3.4 * self.height / 6), sticky="w")
        self.insight_button3 = customtkinter.CTkButton(self.master, text="Open", width=self.width / 4,
                                                       height=self.height / 18, bg_color=self.bg_color,
                                                       command=self.__insight_callback3, fg_color=self.widget_color)
        self.insight_button3.grid(row=0, column=0, padx=(20 + 2 * self.width / 3, 0),
                                  pady=(0, self.height - 4.2 * self.height / 6), sticky="w")

        # #Hotkey registration
        self.macro_button_label = customtkinter.CTkLabel(self.master, text="Trigger button:", bg_color=self.bg_color,
                                                         width=self.width / 3, height=self.height / 18)
        self.macro_button_label.grid(row=0, column=0, padx=(self.left_offset, 0),
                                     pady=(0, self.height - 5.0 * self.height / 6),
                                     sticky="w")
        self.hotkey_window = customtkinter.CTkLabel(self.master, text=self.hotkey, width=self.width / 3 - 10,
                                                    height=self.height / 18, bg_color=self.bg_color,
                                                    fg_color=self.bg_color)
        self.hotkey_window.grid(row=0, column=0, padx=(self.left_offset + self.width / 3, 0),
                                pady=(0, self.height - 5.0 * self.height / 6),
                                sticky="w")
        self.macro_hotkey_register = customtkinter.CTkButton(self.master, text="Register", width=self.width / 4,
                                                             height=self.height / 18, fg_color=self.widget_color,
                                                             command=self.__macro_hotkey_callback,
                                                             bg_color=self.bg_color)
        self.macro_hotkey_register.grid(row=0, column=0, padx=(20 + 2 * self.width / 3, 0),
                                        pady=(0, self.height - 5.0 * self.height / 6),
                                        sticky="w")

        # Checkbox - counter
        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.counter_checkbox = customtkinter.CTkCheckBox(self.master, text="Counter", width=self.width / 3,
                                                          height=self.height / 18,
                                                          onvalue=1, offvalue=0, bg_color=self.bg_color,
                                                          command=self.__counter_callback,
                                                          hover_color="gray20")

        self.counter_checkbox.grid(row=0, column=0, padx=(self.left_offset, 0), pady=(self.height / 6, 0),
                                   sticky="w")

        # Counter - entries

        self.counter_label1 = customtkinter.CTkLabel(self.master, text="Start value", fg_color=self.bg_color,
                                                     width=self.width / 6, height=self.height / 18,
                                                     bg_color=self.bg_color)
        self.counter_label1.grid(row=0, column=0, padx=(1.2 * self.width / 3, 0), pady=(0.5 * self.height / 6, 0),
                                 sticky="w")
        self.counter_entry1 = customtkinter.CTkEntry(self.master, width=self.width / 6, height=self.height / 18,
                                                     border_color=self.widget_color, bg_color=self.bg_color,
                                                     validate='key', validatecommand=vcmd, state="disabled")
        self.counter_entry1.insert(0, 1)
        self.counter_entry1.grid(row=0, column=0, padx=(self.width / 3 + 25, 0), pady=(1.1 * self.height / 6, 0),
                                 sticky="w")
        self.counter_label2 = customtkinter.CTkLabel(self.master, text="Addend", fg_color=self.bg_color,
                                                     width=self.width / 6, height=self.height / 18,
                                                     bg_color=self.bg_color)
        self.counter_label2.grid(row=0, column=0, padx=(2 * self.width / 3 + 5, 0), pady=(0.5 * self.height / 6, 0),
                                 sticky="w")
        self.counter_entry2 = customtkinter.CTkEntry(self.master, width=self.width / 6, height=self.height / 18,
                                                     border_color=self.widget_color, bg_color=self.bg_color,
                                                     validate='key', validatecommand=vcmd, state="disabled")
        self.counter_entry2.insert(0, 1)
        self.counter_entry2.grid(row=0, column=0, padx=(1.8 * self.width / 3 + 25, 0), pady=(1.1 * self.height / 6, 0),
                                 sticky="w")


        # Checkbox - macro working with offset
        self.offset_macro_checkbox = customtkinter.CTkCheckBox(self.master, text="Working with offset", width=50,
                                                               onvalue=1, offvalue=0, bg_color=self.bg_color,
                                                               command=self.__offset_callback,
                                                               height=self.height/18, hover_color="gray20")
        self.offset_macro_checkbox.grid(row=0, column=0, padx=(20, 0), pady=(2*self.height/6, 0), sticky="w")

        # Checkbox - number of macro repeats
        self.repeats_checkbox = customtkinter.CTkCheckBox(self.master, text="Repeatable", width=self.width / 3,
                                                          height=self.height / 18,
                                                          onvalue=1, offvalue=0, bg_color=self.bg_color,
                                                          command=self.__repeats_callback,
                                                          hover_color="gray20")

        self.repeats_checkbox.grid(row=0, column=0, padx=(20, 0), pady=(3 * self.height / 6, 0), sticky="w")

        # Entry - specify the time span between macro steps
        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.pause_label = customtkinter.CTkLabel(self.master, text="Time span between macro steps (s):",
                                                    fg_color=self.bg_color, bg_color=self.bg_color,
                                                    width=2 * self.width / 3, height=self.height / 18)
        self.pause_label.grid(row=0, column=0, padx=(20, 0), pady=(4 * self.height / 6, 0), sticky="w")
        self.pause_entry = customtkinter.CTkEntry(self.master, width=self.width / 6, height=self.height/18,
                                                    border_color=self.widget_color, bg_color=self.bg_color,
                                                    validate='key', validatecommand=vcmd)
        self.pause_entry.insert(0, 0.15)
        self.pause_entry.grid(row=0, column=0, padx=(20 + 3*self.width / 4, 0), pady=(4 * self.height / 6, 0),
                                sticky="w")

        # Button for macro run
        self.run_macro_button = customtkinter.CTkButton(self.master, text="Run", command=self.master.run_macro,
                                                        fg_color=self.run_button_color,
                                                        bg_color=self.bg_color, width=self.width / 2 - 15,
                                                        height=self.height / 12)
        self.run_macro_button.grid(row=0, column=0, padx=(20, 0),
                                   pady=(5 * self.height / 6, 0), sticky="w")

        # Button for listen and run

        self.listen_macro_button = customtkinter.CTkButton(self.master, text="Listen and Run",
                                                           command=self.__listen_macro_callback,
                                                           fg_color=self.run_button_color, bg_color=self.bg_color,
                                                           width=self.width / 2 - 15, height=self.height / 12)
        self.listen_macro_button.grid(row=0, column=0, padx=(self.width / 2 + 15, 0),
                                   pady=(5 * self.height / 6, 0), sticky="w")

        # Tooltip - Macro Filename Entry
        self.macro_filename_entry_tooltip = Hovertip(self.macro_filename_entry,
                                                text="File, where macro will be stored. \n"
                                                     "The name has to end with '.csv' extension")

        # Tooltip - Macro Generator Button
        self.generate_macro_button_tooltip = Hovertip(self.generate_macro_button,
                                                     text="Generates macro in a file specified on the left.\n"
                                                          "If name is not specified, defalut filename is used")

        # Tooltips - Option menus
        self.option_menu1_tooltip = Hovertip(self.option_menu_macro1,
                                             text="Menu for picking macros. Files are stored in a 'macros' folder")
        self.option_menu2_tooltip = Hovertip(self.option_menu_macro2,
                                             text="Menu for picking macros. Files are stored in a 'macros' folder")
        self.option_menu3_tooltip = Hovertip(self.option_menu_macro3,
                                             text="Menu for picking macros. Files are stored in a 'macros' folder")

        # Tooltips - Open Buttons
        self.insight_button1_tooltip = Hovertip(self.insight_button1, text="Opens the file specified on the left")
        self.insight_button2_tooltip = Hovertip(self.insight_button2, text="Opens the file specified on the left")
        self.insight_button3_tooltip = Hovertip(self.insight_button3, text="Opens the file specified on the left")

        #Tooltip - Key register button
        self.macro_hotkey_register_tooltip = Hovertip(self.macro_hotkey_register,
                                                      text="Registers first user's input as a key that will be used\n"
                                                            "by a 'Listen' button. To stop listening for user input press esc.\n"
                                                            "Also esc button cannot be used as a key for macro execution")

        # Tooltip - Counter checkbox
        self.counter_checkbox_tooltip = Hovertip(self.counter_checkbox,
                                                      text="Enables counter - it is incremented by the value in the "
                                                           "'addend' entry at the end of macros' execution process")

        self.counter_entry1_tooltip = Hovertip(self.counter_entry1,
                                                 text="Start value of the counter")

        self.counter_entry2_tooltip = Hovertip(self.counter_entry2,
                                               text="Value that is added to counter at the end of every cycle")

        # Tooltip - Working with offset checkbox
        self.offset_macro_checkbox_tooltip = Hovertip(self.offset_macro_checkbox,
                                                       text="Enables macro execution with object finder.")

        # Tooltip - Repeatable checkbox
        self.repeats_checkbox_tooltip = Hovertip(self.repeats_checkbox,
                                                      text="Enables the option to specify the macro's repeats.")

        # Tooltip - Pause Entry
        self.pause_entry_tooltip = Hovertip(self.pause_entry,
                                                 text="Specifies the pause between every step.")

        # Tooltip - Run Button
        self.run_macro_button_tooltip = Hovertip(self.run_macro_button,
                                            text="Runs macro without 'Object Finder' function")

        # Tooltip - Listen and run
        self.listen_macro_button_tooltip = Hovertip(self.listen_macro_button,
                                            text="Listens for user's input and runs macro, when trigger button is pressed")

    # Callback - generate_macro - uses MacroReader class to listen and generate macro based on user's input
    def __generate_macro_callback(self):
        text = "Click Start to generate macro. \n To stop generating macro press esc"
        pop_up_window = PopUpWindow(self, text)
        self.master.minimize_self()
        filename = self.macro_filename_entry.get()
        macro_recorder.KeyRecorder().record_macro(filename if filename != '' else "macro.csv")
        self.master.maximize_self()
        self.update_optionmenus()
        self.update()

    # Callbacks - option menus and open buttons - pick macro and place it into active macros list
    # Buttons - open current macro for edit
    def __optionmenu1_callback(self, value):
        self.master.active_macros[0] = value
    def __optionmenu2_callback(self, value):
        self.master.active_macros[1] = value
    def __optionmenu3_callback(self, value):
        self.master.active_macros[2] = value

    def __insight_callback1(self):
        try:
            path = str(os.path.dirname(os.path.abspath(__file__))) + "\\macros\\" + self.option_menu_macro1.get()
            os.system(path)
        except Exception as E:
            print(E)
    def __insight_callback2(self):
        try:
            path = str(os.path.dirname(os.path.abspath(__file__))) + "\\macros\\" + self.option_menu_macro2.get()
            os.system(path)
        except Exception as E:
            print(E)
    def __insight_callback3(self):
        try:
            path = str(os.path.dirname(os.path.abspath(__file__))) + "\\macros\\" + self.option_menu_macro3.get()
            os.system(path)
        except Exception as E:
            print(E)

    # Callback - macro hotkey button - registers user input and saves it - program uses the registered key to execute
    # macros when key is detected
    def __macro_hotkey_callback(self):
        key_register = macro_recorder.KeyRegister()
        self.hotkey = key_register.register_key()
        print(self.hotkey)
        # self.hotkey_window.update()
        self.hotkey_window.configure(text=self.hotkey)
        self.hotkey_window.update()
        self.listen_macro_button.configure(state="normal" if self.hotkey != '' else "disabled")

    def __repeats_callback(self):
        if self.repeats_checkbox.get():
            self.repeats_label = customtkinter.CTkLabel(self.master, text="Number of repeats:", fg_color=self.bg_color,
                                                        width=self.width / 3, height=self.height / 18,
                                                        bg_color=self.bg_color)
            self.repeats_label.grid(row=0, column=0, padx=(self.width / 3 + 30, 0), pady=(3 * self.height / 6, 0),
                                    sticky="w")
            self.option_menu_repeats = customtkinter.CTkOptionMenu(self.master, values=[str(n) for n in range(1, 10)],
                                                                   width=self.width / 10,
                                                                   height=self.height / 18, bg_color=self.bg_color,
                                                                   fg_color=self.widget_color)
            self.option_menu_repeats.grid(row=0, column=0, padx=(2 * self.width / 3 + 50, 0),
                                          pady=(3 * self.height / 6, 0),
                                          sticky="w")
        else:
            self.repeats_label.destroy()
            self.option_menu_repeats.destroy()

    # Callback - object_finder_checkbox - disables the RUN button, when checkbox returns 1 and enables user to use
    # macro with object finder
    def __object_finder_checkbox_callback(self):
        self.run_macro_button.configure(state="disabled" if (self.object_finder_checkbox.get() or
                                                             self.offset_macro_checkbox.get()) else "normal")

        self.master.finder = self.object_finder_checkbox.get()
        self.master.object_finder_frame.show_objects_loc_list(self.object_finder_checkbox.get())

    # Callback - offset_macro_checkbox - disables the RUN button, when checkbox returns 1
    def __offset_callback(self):
        self.run_macro_button.configure(state="disabled" if (self.master.object_finder_frame.object_finder_checkbox.get() or
                                                             self.offset_macro_checkbox.get()) else "normal")

    def __counter_callback(self):
        self.counter_entry1.configure(state="normal" if self.counter_checkbox.get() else "disabled")
        self.counter_entry2.configure(state="normal" if self.counter_checkbox.get() else "disabled")
    # Comment

    def __listen_macro_callback(self):
        self.master.minimize_self()
        macro_listener = macro_recorder.KeyRegister()
        print(self.hotkey)
        while macro_listener.listen_for_trigger(self.hotkey):
            print("Triggered!")
            self.master.run_macro()
            macro_listener = macro_recorder.KeyRegister()
        else:
            print("Listening stopped!")
            self.master.maximize_self()
            self.update()

    def show_repeats_window(self):
        self.repeats_entry.configure(state="normal" if self.repeats_checkbox.get() else "disabled")

    def update_optionmenus(self):
        self.macros_list = self.master.list_files("\\macros", ".csv")
        self.option_menu_macro1.configure(values=self.macros_list)
        self.option_menu_macro2.configure(values=self.macros_list)
        self.option_menu_macro3.configure(values=self.macros_list)


                # print(os.path.join(file))

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        """Used for validating user's input in entry"""
        if value_if_allowed:
            try:
                float(value_if_allowed)
                if len(value_if_allowed) < 5:
                    return True
                else:
                    return False
            except ValueError:
                return False
        elif len(value_if_allowed) == 0:
            return True
        else:
            return False


class MacroCreator(customtkinter.CTk):
    """Main window of the app"""
    def __init__(self):
        super().__init__()

        #Configuration
        self.width = 600
        self.height = 400
        self.configure(fg_color="#5299e0")
        self.title("Macro Creator")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.set_window_size()

        #Atributes
        self.macro_reader = macro_executor.MacroReader("key_dictionary.csv")
        self.active_macros = ["---"]*3
        self.objects = []
        self.finder = False
        self.counter_start_value = 0
        self.counter_addend = 0
        self.counter = 0

        # Objects
        self.macro_frame = MacroFrame(self, "Macro")
        self.macro_frame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsew")
        self.object_finder_frame = ObjectFinderFrame(self, "Object Finder")
        self.object_finder_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 10), sticky="nsew")
        self.resizable(0, 0)


    # Iconify window
    def set_window_size(self):
        self.geometry(str(self.width) + "x" + str(self.height))

    def minimize_self(self):
        self.iconify()

    def maximize_self(self):
        self.deiconify()

    def list_files(self, directory, extension):
        """Lists files with a specified extension in a directory"""
        path = str(os.path.dirname(os.path.abspath(__file__))) + directory
        files_list = ["---"]
        for file in os.listdir(path):
            if file.endswith(extension):
                files_list.append(file)
        return files_list
    
    def run_macro(self):
        """"Exetcutes macro for specified conditions"""
        self.minimize_self()
        for macro in self.active_macros:
            if macro != "---":
                self.macro_reader.macro_reader("macros\\" + macro, relative=self.macro_frame.offset_macro_checkbox.get(),
                                               pause=float(self.macro_frame.pause_entry.get()) if
                                               self.macro_frame.pause_entry.get()[-1] != "." else 0.15)

    def run_macro_for_objects(self):
        """"Exetcutes macro for specified conditions for every object found"""

        self.counter_start_value = float(
            self.macro_frame.counter_entry1.get()) if self.macro_frame.counter_checkbox.get() else 0
        self.counter_addend = float(
            self.macro_frame.counter_entry2.get()) if self.macro_frame.counter_checkbox.get() else 0

        self.counter_start_value = int(self.counter_start_value) if self.counter_start_value.is_integer() else self.counter_start_value
        self.counter_addend = int(self.counter_addend) if self.counter_addend.is_integer() else self.counter_addend


        self.counter = self.counter_start_value

        objects = zip(self.objects['X'].to_list(), self.objects['Y'].to_list())
        for obj in objects:
            for macro in self.active_macros:
                if macro != "---":
                    self.macro_reader.macro_reader("macros\\" + macro,
                                                   relative=self.macro_frame.offset_macro_checkbox.get(),
                                                   pause=float(self.macro_frame.pause_entry.get()) if
                                                   self.macro_frame.pause_entry.get()[-1] != "." else 0.15,
                                                   finder=self.finder, object_loc=obj, counter=self.counter)
            self.counter += self.counter_addend
        self.counter = self.counter_start_value

# python -m PyInstaller Model\Macro_builder.py
if __name__ == "__main__":
    app = MacroCreator()
    app.mainloop()



