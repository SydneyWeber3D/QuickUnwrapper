Quick Unwrapper v1.1 How To

Install:
	• If Maya is running, close Maya.
	• Copy QuickUnwrapper.py to Maya's user script directory.
		(e.g. [C:\Users\USERNAME\Documents\maya\MAYAVERSION\scripts])
	• Open Maya.
	• Open Maya's Script Editor [Windows > General Editors > Script Editors].
	• Copy the code between the hashtags (#), excluding the hashtags (#) in a Python tab and run it:

####
import QuickUnwrapper
reload(QuickUnwrapper)
QuickUnwrapper.checkSavedValues()
####

Shelf:
	• Simply click the button labelled "Shelf" after running the script.
		NOTE: Shelf Button should be added in the Poly Modeling tab, immediately after Maya's out-of-the-box UV tools.