import maya.cmds as cmds
import variables as vars
import process as func

safeProjAxis = cmds.optionVar(q="QU_SafetyProjectionAxis")
unwrapMethod = cmds.optionVar(q="QU_Method")
autoAngle = cmds.optionVar(q="QU_AutoAngle")
autoSoften = cmds.optionVar(q="QU_AutoSoften")
textureRes = cmds.optionVar(q="QU_TextureResolution")
texelDens = cmds.optionVar(q="QU_TexelDensity")
shellPad = cmds.optionVar(q="QU_ShellPadding")
tilePad = cmds.optionVar(q="QU_TilePadding")
stackShells = cmds.optionVar(q="QU_StackSimilarShells")

def createWindow():
	if cmds.window("quWindow",ex=True):
		cmds.deleteUI("quWindow",wnd=True)
	if cmds.windowPref("quwindow",ex=True):
		cmds.windowPref("quWindow",r=True)

	cmds.window("quWindow",t="Quick Unwrapper",w=128,h=128,rtf=True,mnb=False,mxb=False,s=False)

	cmds.columnLayout("quContainer",cat=("both",8),cw=256,p="quWindow")
	cmds.separator(w=256,h=8,st="none",p="quContainer")
	# For safety measures, script automatically applies UV projection, ask if the user has any preferred method (Default is Planar across Z axis)
	cmds.frameLayout("safetyFrame",l="Safety Projection Axis",mh=8,cll=True,sbm="Resets the UVs by applying a planar UV projection on the selected mesh.  If the mesh is symmetrical, prefer the axis that crosses the mesh.",p="quContainer")
	cmds.columnLayout("safetyColumn",p="safetyFrame")
	safetyProjectionAxis = cmds.radioButtonGrp(ann="Casts a Planar UV Projection across the selected axis.",la3=["X","Y","Z"],nrb=3,cw3=[50,50,50],sl=safeProjAxis,p="safetyColumn")
	# Ask if the user already has mesh softened/hardened in a UV friendly manner, or if the user pre-selected the edges where they want the seams to be, or if the user wants the script to decide where the seams should be (Method Check)
	cmds.frameLayout("methodFrame",l="Unwrapping Method",mh=8,cll=True,sbm="",p="quContainer")
	cmds.columnLayout("methodMenu",p="methodFrame")
	methodSelect = cmds.optionMenu(ann="Choose which method to use to unwrap mesh.",p="methodMenu")
	cmds.menuItem(l="Automatic",ann="Automatically set edge softness/hardness based on the angle between faces, splits and unwraps the UVs.")
	cmds.menuItem(l="Softness based",ann="Splits the UVs based on user-set hard edges, assuming the hard edges are set where the seams would be.")
	cmds.menuItem(l="Selected edges",ann="Uses the selected edges so split and unwrap the UVs.")
	cmds.optionMenu(methodSelect,e=True,sl=unwrapMethod)
	# If the user wants the automated method, ask the user if they have a preferred angle for auto-smoothing (default 45 degrees); else, disable
	cmds.rowLayout("autoMethodAngle",nc=2,ann="Sets the angle past which edges will be softened.",p="methodFrame")
	cmds.text(l="Softness/Hardness angle: ")
	autoAngle = cmds.floatField(v=autoAngle,min=15.0,max=90.0,w=40,pre=2)
	# If the user wants the pre-selected edges method, ask the user if they would like the script to automatically soften/harden edges based on UV seams
	autoSoften = cmds.checkBox(l=" Soften/Harden Edges",v=autoSoften,ann="If checked, automatically softens and hardens edges based on the UV seams.",p="methodFrame")
	# Request desired map size (1024px by default)
	cmds.frameLayout("mappingFrame",l="Layout Settings",mh=8,cll=True,sbm="",p="quContainer")
	cmds.rowLayout("mapRow",nc=2,p="mappingFrame")
	cmds.text(l="Texture Resolution: ",p="mapRow")
	layoutResolution = cmds.optionMenu(ann="Sets the desired texture resolution for the UVs.",p="mapRow")
	cmds.menuItem(l="8192")
	cmds.menuItem(l="4096")
	cmds.menuItem(l="2048")
	cmds.menuItem(l="1024")
	cmds.menuItem(l="512")
	cmds.menuItem(l="256")
	cmds.menuItem(l="128")
	cmds.menuItem(l="64")
	cmds.menuItem(l="32")
	cmds.menuItem(l="16")
	cmds.menuItem(l="8")
	cmds.optionMenu(layoutResolution,e=True,sl=textureRes)
	# Request Texel Density
	cmds.rowLayout("texelRow",nc=2,ann="Sets the texel density.",p="mappingFrame")
	cmds.text(l="Texel Density (px/u) ",p="texelRow")
	texelDensity = cmds.intField(v=texelDens,min=0,max=64,w=40,p="texelRow")
	# Request shell padding (4px by default) and tile padding (8px by default)
	cmds.rowLayout("shellRow",nc=2,ann="Sets the padding around each UV shells, the minimum space between UV shells should be the set value multiplied by two.",p="mappingFrame")
	cmds.text(l="Shell padding (pixels) ",p="shellRow")
	shellPadding = cmds.intField(v=shellPad,min=0,max=256,w=40,p="shellRow")
	cmds.rowLayout("tileRow",nc=2,ann="Sets the padding around the UV space.",p="mappingFrame")
	cmds.text(l="Tile padding (pixels) ",p="tileRow")
	tilePadding = cmds.intField(v=tilePad,min=0,max=256,w=40,p="tileRow")
	# Ask if the user desires to have similar UV shells stacked
	cmds.rowLayout("stackRow",nc=2,p="mappingFrame")
	stackSimilar = cmds.checkBox(l=" Stack similar shells",v=stackShells,ann="If checked, will stack similar shells together to save UV space.")
	# Apply unwrap, or Cancel and close buttons
	cmds.setParent("quContainer")
	cmds.separator(w=256,h=8,st="none")
	cmds.rowLayout("buttonsRow",nc=3,p="quContainer")
	cmds.button(l="Unwrap",w=64,h=32,ann="Process the request and unwrap selected mesh.",c=(lambda *args:func.processRequest()))
	cmds.button(l="Cancel",w=64,h=32,ann="Cancel and close script.",c=("cmds.deleteUI(\"quWindow\",wnd=True); cmds.windowPref(\"quWindow\",r=True)"))
	cmds.button(l="Shelf",w=32,h=32,ann="Create shelf icon.",c=(lambda *args:addShelfIcon()))
	cmds.separator(w=256,h=8,st="none",p="quContainer")

	cmds.showWindow("quWindow")

class _shelf():
	def __init__(self, shelfName="Polygons", iconPath=""):
		self.shelfName = shelfName
		self.iconPath = iconPath
		cmds.setParent(self.shelfName)

		self.build()

	def build(self):
		pass

	def addButton(self, label, icon="QU_ShelfIcon.png"):
		cmds.setParent(self.shelfName)
		if icon:
			icon = self.iconPath + icon
			cmds.shelfButton(w=32,h=32,i=icon,l=label,mi=("Quick Run", "print \"Quick Run\""),mi=("Settings", "print \"Open Settings\""),c="print \"Run Script\"",dcc="print \"Open Settings 2\"",st="iconOnly")

class addShelfIcon(_shelf):
	def build(self):
		self.addButton(label="Quick Unwrapper")