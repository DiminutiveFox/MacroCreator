# Macro Creator 
It increases productivity and simplifies time-consuming and repetitive tasks. 
Personally it helped me during SCADA development process (visualisation of a factory) 

# Project description
Project contains 2 main areas - Macro Generator and Object Finder. Macro Generator is meant for creating and running macros, when Object Finder looks for a determined object on the screen and finds it's coordinates - then macro can be performed upon it. 

![image](https://github.com/DiminutiveFox/Macro-Creator/assets/135659343/f31da4f3-188c-4785-9103-0875973bbd3b)

# Macro Generator
It creates a macros that can be executed in a multiple ways. It registers user's mouse and keyboard input and stores it in a .csv file in a 'macros' directory. 
Application uses it to execute the macro when trigger key is pressed - user can also specify the trigger button using 'Key Register' function.

![image](https://github.com/DiminutiveFox/Macro-Creator/assets/135659343/29445c39-1427-4b89-9081-2e5e49b9885b)

In drop-down menus, user can pick up to 3 different macros that will be executed in a single run. 
User can select 'Working with offset' function that calculates mouse movements based on a loaded macro and current mouse position so that mouse will run with an 'offset'.
User can specify the number of repeats - after macro execution it will be repeated as many times as it is specified in the drop-down menu. 

# Object Finder
It takes a picture of a screen and looks for objects defined in a drop down menus. Objects screenshots have to be placed in the 'images' directory. It has to be done manually (Windows eg. pressing 'Shift + Win + S').
Filename has to end with a .csv extension - otherwise the coordinates won't be saved. User needs to determine the accuracy coefficient - it has to be between 0 and 0.99 - the lower the value, the more positive falses 
will be found; the higher the value, the more false positives.

![image](https://github.com/DiminutiveFox/Macro-Creator/assets/135659343/fe0d9bba-b8f8-4f01-811b-038734c145e8)

Files are stored in a 'locations' directory. Application also creates and shows a picture with object that were found - objects are indicated by green squares. User can validate and play with accuracy coefficient to improve the results. However the file cannot be picked in the drop-down menu unless the 'Working with object finder' checkbox in Macro Creator area is picked. 
Start button is enabled when correct file is picked in drop-down menu. Also 'Working with offset' and "Repeatable' checkboxes are applied here. 
