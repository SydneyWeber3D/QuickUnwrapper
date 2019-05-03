import maya.cmds as cmds

import variables as vars
vars.check()

import interface as menu
menu.createWindow()

import process as func

#	Skips generating the window and runs the script using the last user settings.
def quickRun():
	vars.check()
	func.processRequest()

#	Opens the window, allowing the user to tweak their settings accordingly.
def fullRun():
	vars.check()
	menu.createWindow()