import maya.cmds as cmds

def _null(*args):
	pass

class _shelf():
	def __init__(self, shelfName="Polygons", iconPath=""):
		self.shelfName = shelfName
		self.iconPath = iconPath
		cmds.setParent(self.shelfName)

		self.build()

	def build(self):
		pass

	def addButton(self, label, icon="QU_shelfIcon.png"):
		cmds.setParent(self.shelfName)
		if icon:
			icon = self.iconPath + icon
			cmds.shelfButton(w=32,h=32,i=icon,l=label,mi=("Settings", "print \"Open Settings\""),c="print \"Run Script\"",dcc="print \"Open Settings 2\"",st="iconOnly")

class addShelfIcon(_shelf):
	def build(self):
		self.addButton(label="Quick Unwrapper")

addShelfIcon()