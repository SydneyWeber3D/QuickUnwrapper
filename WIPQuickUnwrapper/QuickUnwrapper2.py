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

	cmds.columnLayout("quContainer",cat=("both",8),cw=256,p="quWindow")
	# For safety measures, script automatically applies UV projection, ask if the user has any preferred method (Default is Planar across Z axis)
	cmds.frameLayout("safetyFrame",l="Safety Projection Axis",mh=8,cll=True,sbm="Resets the UVs by applying a planar UV projection on the selected mesh.  If the mesh is symmetrical, prefer the axis that crosses the mesh.",p="quContainer")
	cmds.rowLayout("sfRow",nc=3,p="safetyFrame")
	safetyProjectionAxis = cmds.radioCollection(p="sfRow")
	spaX = cmds.radioButton(l="X",w=50,sl=False)
	spaY = cmds.radioButton(l="Y",w=50,sl=False)
	spaZ = cmds.radioButton(l="Z",w=50,sl=True)
	# Ask if the user already has mesh softened/hardened in a UV friendly manner, or if the user pre-selected the edges where they want the seams to be, or if the user wants the script to decide where the seams should be (Method Check)
	cmds.frameLayout("methodFrame",l="Unwrapping Method",mh=8,cll=True,sbm="",p="quContainer")
	cmds.columnLayout("methodMenu",p="methodFrame")
	methodSelect = cmds.optionMenu(p="methodMenu")
	cmds.menuItem(l="Automatic")
	cmds.menuItem(l="Softness based")
	cmds.menuItem(l="Selected edges")
	# If the user wants the pre-selected edges method, ask the user if they would like the script to automatically soften/harden edges based on UV seams
	cmds.separator(w=256,h=8,st="none")
	autoSoften = cmds.checkBox(l=" Soften/Harden Edges",en=False)
	# If the user wants the automated method, ask the user if they have a preferred angle for auto-smoothing (default 45 degrees); else, disable
	cmds.rowLayout("autoMethodAngle",nc=2,p="methodFrame")
	cmds.text(l="Softness/Hardness angle: ",en=False)
	automaticAngle = cmds.floatField(v=45.0,min=30.0,max=60.0,w=64,pre=2,en=False)
	# Request desired map size (1024px by default)
	cmds.frameLayout("mappingFrame",l="Layout Settings",mh=8,cll=True,sbm="",p="quContainer")
	cmds.rowLayout("mapRow",nc=2,p="mappingFrame")
	cmds.text(l="Texture Resolution: ",p="mapRow")
	layoutResolution = cmds.optionMenu(p="mapRow")
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
	# Request shell padding (4px by default) and tile padding (8px by default)
	cmds.rowLayout("shellRow",nc=2,p="mappingFrame")
	cmds.text(l="Shell padding",p="shellRow")
	shellPadding = cmds.intField(v=4,min=0,max=64,w=32,p="shellRow")
	cmds.rowLayout("tileRow",nc=2,p="mappingFrame")
	cmds.text(l="Tile padding",p="tileRow")
	tilePadding = cmds.intField(v=8,min=0,max=64,w=32,p="tileRow")
	# Ask if the user desires to have similar UV shells stacked
	cmds.rowLayout("stackRow",nc=2,p="mappingFrame")
	stackSimilar = cmds.checkBox(l=" Stack similar shells")
	# Apply unwrap, or Cancel and close buttons
	cmds.setParent("quContainer")
	cmds.separator(w=256,h=16,st="none")
	cmds.rowLayout("buttonsRow",nc=3,p="quContainer")
	cmds.button(l="Unwrap",w=64,h=32,ann="Process the request and unwrap selected mesh.",c=(lambda args: processRequest()))
	cmds.button(l="Cancel",w=64,h=32,ann="Cancel and close script.",c=("cmds.deleteUI(\"quWindow\",wnd=True); cmds.windowPref(\"quWindow\",r=True)"))
	# Option to generate shelf button
	cmds.button(l="?",w=24,h=24,ann="Add QuickUnwrapper to the current shelf.",c=(lambda args: makeShelfButton()))

	cmds.showWindow("quWindow")

def processRequest():
	# Set progress bar
	selectionBuffer = cmds.ls(sl=True,tr=True,tl=1,sn=True)
	selectedMesh = selectionBuffer[0]
	# Apply safety UV Projection (Planar Z?)
	safetyProjection(selectedMesh)
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

def safetyProjection(selectedMesh):
	# Apply safety UV Projection (Planar Z?)
	cmds.select(selectedMesh+".f[*]")
	facesBuffer = cmds.ls(sl=True,tl=1)
	meshFaces = facesBuffer[0]
	cmds.select(cl=True)

	cmds.polyProjection(meshFaces,ch=False,t="Planar",md="z")

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