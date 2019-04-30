import maya.cmds as cmds

import variables as vars
vars.check()

import interface as menu
menu.createWindow()

import process as func

def quickRun():
	vars.check()
	func.processRequest()

def fullRun():
	vars.check()
	menu.createWindow()