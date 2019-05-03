Quick Unwrapper v1.3 How To

Install:
	• If Maya is running, close Maya.
	• Copy both the [prefs] and [scripts] folders to your Maya version's user directory.
		(e.g. [C:\Users\USERNAME\Documents\maya\MAYAVERSION])
	• Open Maya.
	• Open Maya's Script Editor [Windows > General Editors > Script Editors].
		Note: You can also use the mini-command input field at the lower left-hand corner of Maya's default layout, just make sure to switch it from MEL to Python beforehand by simply clicking the label.
	• Copy the code between the hashtags (#), excluding the hashtags (#) in a Python tab and run it:

####
import QuickUnwrapper
####

Shelf:
	• Simply click the button labelled "Shelf" after running the script.
		NOTE: Shelf Button should be added in the Poly Modeling tab, immediately after Maya's out-of-the-box UV tools.
	• A single left-click on the shelf button runs the script with the last input settings.
		Note: Opening the script's settings window, changing settings, then closing the window or pressing the "Cancel" button will not save user input settings.  User input settings are only saved upon pressing the "Unwrap" button.
	• A double left-click on the shelf button opens the script's settings window.
	• A right-click then click on the "Settings" option opens the script's settings window.