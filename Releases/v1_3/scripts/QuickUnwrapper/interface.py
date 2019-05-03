import maya.cmds as cmds
import process as func

def createWindow():
	if cmds.window("quWindow",ex=True):
		cmds.deleteUI("quWindow",wnd=True)
	if cmds.windowPref("quwindow",ex=True):
		cmds.windowPref("quWindow",r=True)
	
	if cmds.optionVar(q="QU_AutoSoften") == "True":
		autoSoften = 1
	else:
		autoSoften = 0
	if cmds.optionVar(q="QU_StackSimilarShells") == "True":
		stackShells = 1
	else:
		stackShells = 0
	
	if cmds.optionVar(q="QU_Method") == 1:
		autoAngleState = True
		autoSoftenState = False
	elif cmds.optionVar(q="QU_Method") == 3:
		autoAngleState = False
		autoSoftenState = True
	else:
		autoAngleState = False
		autoSoftenState = False

	cmds.window("quWindow",t="Quick Unwrapper",w=64,h=64,rtf=True,mnb=False,mxb=False,s=False)
	cmds.showWindow("quWindow")

	cmds.columnLayout("quContainer",cat=("both",8),cw=256,p="quWindow")
	cmds.separator(w=256,h=8,st="none",p="quContainer")
	# For safety measures, script automatically applies UV projection, ask if the user has any preferred method (Default is Planar across Z axis)
	cmds.frameLayout("safetyFrame",l="Safety Projection Axis",mh=8,cll=True,sbm="Resets the UVs by applying a planar UV projection on the selected mesh.  If the mesh is symmetrical, prefer the axis that crosses the mesh.",p="quContainer")
	cmds.columnLayout("safetyColumn",p="safetyFrame")
	setSPA = cmds.radioButtonGrp(ann="Casts a Planar UV Projection across the selected axis.  Recommended: Camera.",la4=["X","Y","Z","Camera"],nrb=4,cw4=[40,40,40,60],sl=cmds.optionVar(q="QU_SafetyProjectionAxis"),p="safetyColumn")
	# Ask if the user already has mesh softened/hardened in a UV friendly manner, or if the user pre-selected the edges where they want the seams to be, or if the user wants the script to decide where the seams should be (Method Check)
	cmds.frameLayout("methodFrame",l="Unwrapping Method",mh=8,cll=True,sbm="",p="quContainer")
	cmds.columnLayout("methodMenu",p="methodFrame")
	setMethod = cmds.optionMenu(ann="Choose which method to use to unwrap mesh.",cc=(lambda *args:updateWindow(setMethod,autoAngleLabel,setAutoAngle,setAutoSoften)),p="methodMenu")
	cmds.menuItem(l="Automatic",ann="Automatically set edge softness/hardness based on the angle between faces, splits and unwraps the UVs.")
	cmds.menuItem(l="Softness based",ann="Splits the UVs based on user-set hard edges, assuming the hard edges are set where the seams would be.")
	cmds.menuItem(l="Selected edges",ann="Uses the selected edges so split and unwrap the UVs.")
	cmds.optionMenu(setMethod,e=True,sl=cmds.optionVar(q="QU_Method"))
	# If the user wants the automated method, ask the user if they have a preferred angle for auto-smoothing (default 45 degrees); else, disable
	cmds.rowLayout("autoMethodAngle",nc=2,ann="Sets the angle past which edges will be softened.",p="methodFrame")
	autoAngleLabel = cmds.text("autoAngleLabel",l="Softness/Hardness angle ",en=autoAngleState)
	setAutoAngle = cmds.floatField("autoAngleInput",v=cmds.optionVar(q="QU_AutoAngle"),min=15.0,max=90.0,w=40,pre=2,en=autoAngleState)
	# If the user wants the pre-selected edges method, ask the user if they would like the script to automatically soften/harden edges based on UV seams
	setAutoSoften = cmds.checkBox("autoSoftenInput",l=" Soften/Harden Edges",v=autoSoften,ann="If checked, automatically softens and hardens edges based on the UV seams.",en=autoSoftenState,p="methodFrame")
	# Request desired map size (1024px by default)
	cmds.frameLayout("mappingFrame",l="Layout Settings",mh=8,cll=True,sbm="",p="quContainer")
	cmds.rowLayout("mapRow",nc=2,p="mappingFrame")
	cmds.text(l="Texture Resolution ",p="mapRow")
	setLayoutResolution = cmds.optionMenu(ann="Sets the desired texture resolution for the UVs.",p="mapRow")
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
	cmds.optionMenu(setLayoutResolution,e=True,sl=cmds.optionVar(q="QU_TextureResolutionID"))
	# Request shell padding (4px by default) and tile padding (8px by default)
	cmds.rowLayout("shellRow",nc=2,ann="Sets the padding around each UV shells.",p="mappingFrame")
	cmds.text(l="Shell padding (pixels) ",p="shellRow")
	setShellPadding = cmds.intField(v=cmds.optionVar(q="QU_ShellPadding"),min=0,max=256,w=40,p="shellRow")
	cmds.rowLayout("tileRow",nc=2,ann="Sets the padding around the UV space.",p="mappingFrame")
	cmds.text(l="Tile padding (pixels) ",p="tileRow")
	setTilePadding = cmds.intField(v=cmds.optionVar(q="QU_TilePadding"),min=0,max=256,w=40,p="tileRow")
	# Apply unwrap, or Cancel and close buttons
	cmds.setParent("quContainer")
	cmds.separator(w=256,h=8,st="none")
	cmds.rowLayout("buttonsRow",nc=3,p="quContainer")
	cmds.button(l="Unwrap",w=64,h=32,ann="Process the request and unwrap selected mesh.",c=(lambda *args:convertVars(setSPA,setMethod,setAutoAngle,setAutoSoften,setLayoutResolution,setShellPadding,setTilePadding)))
	cmds.button(l="Cancel",w=64,h=32,ann="Cancel and close script.",c=("cmds.deleteUI(\"quWindow\",wnd=True); cmds.windowPref(\"quWindow\",r=True)"))
	cmds.button(l="Shelf",w=32,h=32,ann="Create shelf icon.",c=(lambda *args:addShelfIcon()))
	cmds.separator(w=256,h=8,st="none",p="quContainer")

def updateWindow(chosenMethod,autoAngleLabel,autoAngleInput,autoSoftenInput):
	methodValue = cmds.optionMenu(chosenMethod,q=True,v=True)
	if methodValue == "Automatic":
		cmds.text(autoAngleLabel,e=True,en=True)
		cmds.floatField(autoAngleInput,e=True,en=True)
		cmds.checkBox(autoSoftenInput,e=True,en=False)
	elif methodValue == "Selected edges":
		cmds.text(autoAngleLabel,e=True,en=False)
		cmds.floatField(autoAngleInput,e=True,en=False)
		cmds.checkBox(autoSoftenInput,e=True,en=True)
	else:
		cmds.text(autoAngleLabel,e=True,en=False)
		cmds.floatField(autoAngleInput,e=True,en=False)
		cmds.checkBox(autoSoftenInput,e=True,en=False)

def addShelfIcon():
	shelfTab = "Polygons"
	icon = "QU_ShelfIcon.png"
	label = "Quick Unwrapper v1.3"

	cmds.setParent(shelfTab)
	cmds.shelfButton(w=32,h=32,i=icon,l=label,mi=("Settings", "python(\"import QuickUnwrapper\");python(\"QuickUnwrapper.fullRun()\");"),c="import QuickUnwrapper\nQuickUnwrapper.quickRun()",dcc="import QuickUnwrapper\nQuickUnwrapper.fullRun()",st="iconOnly")
	
def convertVars(setSPA,setMethod,setAutoAngle,setAutoSoften,setLayoutResolution,setShellPadding,setTilePadding):
	cmds.optionVar(iv=("QU_SafetyProjectionAxis",cmds.radioButtonGrp(setSPA,q=True,sl=True)))
	cmds.optionVar(iv=("QU_Method",cmds.optionMenu(setMethod,q=True,sl=True)))
	cmds.optionVar(fv=("QU_AutoAngle",cmds.floatField(setAutoAngle,q=True,v=True)))
	cmds.optionVar(sv=("QU_AutoSoften",cmds.checkBox(setAutoSoften,q=True,v=True)))
	cmds.optionVar(iv=("QU_TextureResolutionID",cmds.optionMenu(setLayoutResolution,q=True,sl=True)))
	cmds.optionVar(iv=("QU_TextureResolution",int(cmds.optionMenu(setLayoutResolution,q=True,v=True))))
	cmds.optionVar(iv=("QU_ShellPadding",cmds.intField(setShellPadding,q=True,v=True)))
	cmds.optionVar(iv=("QU_TilePadding",cmds.intField(setTilePadding,q=True,v=True)))
	
	func.processRequest()