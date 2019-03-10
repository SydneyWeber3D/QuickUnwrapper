import maya.cmds as cmds
import maya.mel as mmel

'''
import QuickUnwrapper
reload(QuickUnwrapper)
QuickUnwrapper.quWindow()
'''

def quWindow():
	if cmds.window("quWindow",ex=True):
		cmds.deleteUI("quWindow",wnd=True)
	if cmds.windowPref("quwindow",ex=True):
		cmds.windowPref("quWindow",r=True)

    # Draw first-launch/options window
    cmds.window("quWindow",t="Quick Unwrapper",rtf=True,mnb=False,mxb=False,s=True)
    cmds.columnLayout("quContainer",cat=("both",10),cw=200,p="quWindow")
    # For safety measures, script automatically applies UV projection, ask if the user has any preferred method (Default is Planar across Z axis)
    # Ask if the user already has mesh softened/hardened in a UV friendly manner, or if the user pre-selected the edges where they want the seams to be, or if the user wants the script to decide where the seams should be (Method Check)
    # If the uses wants the pre-selected edges method, ask the user if they would like the script to automatically soften/harden edges based on UV seams
    # If the user wants the automated method, ask the user if they have a preferred angle for auto-smoothing (default 45 degrees); else, disable
    # Request desired map size (1024px by default)
    # Request shell padding (4px by default) and tile padding (8px by default)
    # Ask if the user desires to have similar UV shells stacked
    # Apply unwrap, or Cancel and close buttons
    # Option to generate shelf button

def processRequest():
    # Set progress bar
    # Apply safety UV Projection (Planar Z?)
    # Increment progress bar
    # If mesh pre-softened/hardened, skip; if user wants to use selected edges, switch to edge selection; else, apply auto mesh softness based on input (default 45 degrees)
    # Increment progress bar
    # If user wants to use selected edges, use old method; else, apply auto-seams
    # Increment progress bar
    # Apply Unfold3D
    # Increment progress bar
    # Apply Unfold Legacy step 1
    # Increment progress bar
    # Apply Unfold Legacy step 2
    # Increment progress bar
    # Apply UV Optimization
    # Increment progress bar
    # Apply Layout step 1
    # Increment progress bar
    # Apply shell Orientation
    # Increment progress bar
    # Apply Layout step 2
    # Increment progress bar
    # If user chose selected edges method, soften/harden edges based on selection; else, skip
    # Complete progress bar, then remove

def safetyProjection():
    # Apply safety UV Projection (Planar Z?)

def methodCheck():
    # If mesh pre-softened/hardened, skip; if user wants to use selected edges, switch to edge selection; else, apply auto mesh softness based on input (default 45 degrees)

def edgeSelectionMethod():
    # If user wants to use selected edges, use old method; else, apply auto-seams

def autoSeamMethod():
    # If user wants to use selected edges, use old method; else, apply auto-seams

def unfoldProcess():
    # Apply Unfold3D
    # then
    # Apply Unfold Legacy step 1
    # then
    # Apply Unfold Legacy step 2

def optimizationStep():
    # Apply UV Optimization

def layoutProcess():
    # Apply Layout step 1
    # then
    # Apply Layout step 2

def orientationStep():
    # Apply shell Orientation

def autoSoftenHarden():
    # If user chose selected edges method, soften/harden edges based on selection; else, skip

def makeShelfButton():
    # Generate shelf button if user decided so
    # Shelf button should generate either in custom tab or alongside Maya's UV mapping shelf tools in poly modeling tab

quWindow()