###########################################################################
# Quick Unwrapper version 1.1											  #
# Sydney Weber															  #
# Repository available at https://github.com/SydneyWeber3D/QuickUnwrapper #
###########################################################################

'''
import QuickUnwrapper
reload(QuickUnwrapper)
QuickUnwrapper.checkSavedValues()
'''

import maya.cmds as cmds

def checkSavedValues():
	if cmds.optionVar(ex="quickUnwrapperSafetyProjectionAxis"):
		setProjAxis = cmds.optionVar(q="quickUnwrapperSafetyProjectionAxis")
	else:
		setProjAxis = 3
	if cmds.optionVar(ex="quickUnwrapperMethod"):
		setMethod = cmds.optionVar(q="quickUnwrapperMethod")
	else:
		setMethod = 1
	if cmds.optionVar(ex="quickUnwrapperAutoAngle"):
		setAngle = cmds.optionVar(q="quickUnwrapperAutoAngle")
	else:
		setAngle = 60.00
	if cmds.optionVar(ex="quickUnwrapperAutoSoften"):
		setSoftness = cmds.optionVar(q="quickUnwrapperAutoSoften")
	else:
		setSoftness = 0
	if cmds.optionVar(ex="quickUnwrapperTextureResolution"):
		setResolution = cmds.optionVar(q="quickUnwrapperTextureResolution")
	else:
		setResolution = 3
	if cmds.optionVar(ex="quickUnwrapperTexelDensity"):
		setTexDensity = cmds.optionVar(q="quickUnwrapperTexelDensity")
	else:
		setTexDensity = 0
	if cmds.optionVar(ex="quickUnwrapperShellPadding"):
		setShellPad = cmds.optionVar(q="quickUnwrapperShellPadding")
	else:
		setShellPad = 4
	if cmds.optionVar(ex="quickUnwrapperTilePadding"):
		setTilePad = cmds.optionVar(q="quickUnwrapperTilePadding")
	else:
		setTilePad = 8
	if cmds.optionVar(ex="quickUnwrapperStackSimilarShells"):
		setShellStack = cmds.optionVar(q="quickUnwrapperStackSimilarShells")
	else:
		setShellStack = 0
	
	quWindow(setProjAxis,setMethod,setAngle,setSoftness,setResolution,setTexDensity,setShellPad,setTilePad,setShellStack)

def quWindow(setProjAxis,setMethod,setAngle,setSoftness,setResolution,setTexDensity,setShellPad,setTilePad,setShellStack):
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
	safetyProjectionAxis = cmds.radioButtonGrp(ann="Casts a Planar UV Projection across the selected axis.",la3=["X","Y","Z"],nrb=3,cw3=[50,50,50],sl=setProjAxis,p="safetyColumn")
	# Ask if the user already has mesh softened/hardened in a UV friendly manner, or if the user pre-selected the edges where they want the seams to be, or if the user wants the script to decide where the seams should be (Method Check)
	cmds.frameLayout("methodFrame",l="Unwrapping Method",mh=8,cll=True,sbm="",p="quContainer")
	cmds.columnLayout("methodMenu",p="methodFrame")
	methodSelect = cmds.optionMenu(ann="Choose which method to use to unwrap mesh.",p="methodMenu")
	cmds.menuItem(l="Automatic",ann="Automatically set edge softness/hardness based on the angle between faces, splits and unwraps the UVs.")
	cmds.menuItem(l="Softness based",ann="Splits the UVs based on user-set hard edges, assuming the hard edges are set where the seams would be.")
	cmds.menuItem(l="Selected edges",ann="Uses the selected edges so split and unwrap the UVs.")
	cmds.optionMenu(methodSelect,e=True,sl=setMethod)
	# If the user wants the automated method, ask the user if they have a preferred angle for auto-smoothing (default 45 degrees); else, disable
	cmds.rowLayout("autoMethodAngle",nc=2,ann="Sets the angle past which edges will be softened.",p="methodFrame")
	cmds.text(l="Softness/Hardness angle: ")
	autoAngle = cmds.floatField(v=setAngle,min=15.0,max=90.0,w=40,pre=2)
	# If the user wants the pre-selected edges method, ask the user if they would like the script to automatically soften/harden edges based on UV seams
	autoSoften = cmds.checkBox(l=" Soften/Harden Edges",v=setSoftness,ann="If checked, automatically softens and hardens edges based on the UV seams.",p="methodFrame")
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
	cmds.optionMenu(layoutResolution,e=True,sl=setResolution)
	# Request Texel Density
	cmds.rowLayout("texelRow",nc=2,ann="Sets the texel density.",p="mappingFrame")
	cmds.text(l="Texel Density (px/u) ",p="texelRow")
	texelDensity = cmds.intField(v=setTexDensity,min=0,max=64,w=40,p="texelRow")
	# Request shell padding (4px by default) and tile padding (8px by default)
	cmds.rowLayout("shellRow",nc=2,ann="Sets the padding around each UV shells, the minimum space between UV shells should be the set value multiplied by two.",p="mappingFrame")
	cmds.text(l="Shell padding (pixels) ",p="shellRow")
	shellPadding = cmds.intField(v=setShellPad,min=0,max=256,w=40,p="shellRow")
	cmds.rowLayout("tileRow",nc=2,ann="Sets the padding around the UV space.",p="mappingFrame")
	cmds.text(l="Tile padding (pixels) ",p="tileRow")
	tilePadding = cmds.intField(v=setTilePad,min=0,max=256,w=40,p="tileRow")
	# Ask if the user desires to have similar UV shells stacked
	cmds.rowLayout("stackRow",nc=2,p="mappingFrame")
	stackSimilar = cmds.checkBox(l=" Stack similar shells",v=setShellStack,ann="If checked, will stack similar shells together to save UV space.")
	# Apply unwrap, or Cancel and close buttons
	cmds.setParent("quContainer")
	cmds.separator(w=256,h=8,st="none")
	cmds.rowLayout("buttonsRow",nc=3,p="quContainer")
	cmds.button(l="Unwrap",w=64,h=32,ann="Process the request and unwrap selected mesh.",c=(lambda args: checkVars(safetyProjectionAxis,methodSelect,autoAngle,autoSoften,layoutResolution,texelDensity,shellPadding,tilePadding,stackSimilar)))
	cmds.button(l="Cancel",w=64,h=32,ann="Cancel and close script.",c=("cmds.deleteUI(\"quWindow\",wnd=True); cmds.windowPref(\"quWindow\",r=True)"))
	cmds.button(l="Shelf",w=32,h=32,ann="Create shelf icon.",c=(lambda args:addShelfIcon()))
	cmds.separator(w=256,h=8,st="none",p="quContainer")

	cmds.showWindow("quWindow")

def checkVars(safetyProjectionAxis,methodSelect,autoAngle,autoSoften,layoutResolution,texelDensity,shellPadding,tilePadding,stackSimilar):
	
	print safetyProjectionAxis
	print methodSelect
	print autoAngle
	print autoSoften
	print layoutResolution
	print texelDensity
	print shellPadding
	print tilePadding
	print stackSimilar
	print "========"
	
	quickUnwrapperSafetyProjection = cmds.radioButtonGrp(safetyProjectionAxis,q=True,sl=True)
	quickUnwrapperMethod = cmds.optionMenu(methodSelect,q=True,sl=True)
	quickUnwrapperAutoAngle = cmds.floatField(autoAngle,q=True,v=True)
	quickUnwrapperAutoSoften = cmds.checkBox(autoSoften,q=True,v=True)
	quickUnwrapperTextureResolution = cmds.optionMenu(layoutResolution,q=True,sl=True)
	quickUnwrapperTexelDensity = cmds.intField(texelDensity,q=True,v=True)
	quickUnwrapperShellPadding = cmds.intField(shellPadding,q=True,v=True)
	quickUnwrapperTilePadding = cmds.intField(tilePadding,q=True,v=True)
	quickUnwrapperStackSimilarShells = cmds.checkBox(stackSimilar,q=True,v=True)

	cmds.optionVar(iv=("quickUnwrapperSafetyProjectionAxis",quickUnwrapperSafetyProjection))
	cmds.optionVar(iv=("quickUnwrapperMethod",quickUnwrapperMethod))
	cmds.optionVar(fv=("quickUnwrapperAutoAngle",quickUnwrapperAutoAngle))
	cmds.optionVar(iv=("quickUnwrapperAutoSoften",quickUnwrapperAutoSoften))
	cmds.optionVar(iv=("quickUnwrapperTextureResolution",quickUnwrapperTextureResolution))
	cmds.optionVar(iv=("quickUnwrapperTexelDensity",quickUnwrapperTexelDensity))
	cmds.optionVar(iv=("quickUnwrapperShellPadding",quickUnwrapperShellPadding))
	cmds.optionVar(iv=("quickUnwrapperTilePadding",quickUnwrapperTilePadding))
	cmds.optionVar(iv=("quickUnwrapperStackSimilarShells",quickUnwrapperStackSimilarShells))

	print "Safety Projection Axis (1=x, 2=y, 3=z)" + str(cmds.optionVar(q="quickUnwrapperSafetyProjectionAxis"))
	print "Method (1=automatic, 2=softness, 3=edge selection) " + str(cmds.optionVar(q="quickUnwrapperMethod"))
	print "Auto Angle " + str(cmds.optionVar(q="quickUnwrapperAutoAngle"))
	print "Auto Soften " + str(cmds.optionVar(q="quickUnwrapperAutoSoften"))
	print "Texture Resolution " + str(cmds.optionVar(q="quickUnwrapperTextureResolution"))
	print "Texture Density (px/u) " + str(cmds.optionVar(q="quickUnwrapperTexelDensity"))
	print "Shell Padding (px) " + str(cmds.optionVar(q="quickUnwrapperShellPadding"))
	print "Tile Padding (px) " + str(cmds.optionVar(q="quickUnwrapperTilePadding"))
	print "Stack Similar Shells " + str(cmds.optionVar(q="quickUnwrapperStackSimilarShells"))

	processRequest(quickUnwrapperSafetyProjection,quickUnwrapperMethod,quickUnwrapperAutoAngle,quickUnwrapperAutoSoften,quickUnwrapperTextureResolution,quickUnwrapperShellPadding,quickUnwrapperTilePadding,quickUnwrapperStackSimilarShells)

def processRequest(quickUnwrapperSafetyProjection,quickUnwrapperMethod,quickUnwrapperAutoAngle,quickUnwrapperAutoSoften,quickUnwrapperTextureResolution,quickUnwrapperShellPadding,quickUnwrapperTilePadding,quickUnwrapperStackSimilarShells):
	# Save current selection
	print "Process Request..."
	# selectionBuffer = cmds.ls(sl=True,tr=True,tl=1,sn=True)
	selectionBuffer = cmds.ls(sl=True)
	print selectionBuffer
	print "selectionBuffer[0]: " + selectionBuffer[0]
	if quickUnwrapperMethod == 2:
		splitSelection = selectionBuffer[0].split('.')
		selectedMesh = splitSelection[0]
		selectedEdges = 0
	elif quickUnwrapperMethod == 3:
		selectedEdges = selectionBuffer
		selectionSplit = selectionBuffer[0].split('.')
		selectedMesh = selectionSplit[0]
	else:
		selectedMesh = selectionBuffer[0]
		selectedEdges = 0
	print "Selected mesh is: " + selectedMesh
	# Apply safety UV Projection (Planar Z?)
	safetyProjection(selectedMesh,quickUnwrapperSafetyProjection)
	# If mesh pre-softened/hardened, skip; if user wants to use selected edges, switch to edge selection; else, apply auto mesh softness based on input (default 45 degrees)
	methodCheck(selectedMesh,selectedEdges,quickUnwrapperMethod,quickUnwrapperAutoAngle,quickUnwrapperAutoSoften)
	# Apply Unfold3D
	unfoldProcess(selectedMesh,quickUnwrapperTextureResolution,quickUnwrapperTilePadding)
	# Apply UV Optimization
	optimizationStep(selectedMesh,quickUnwrapperTextureResolution,quickUnwrapperTilePadding)
	# Apply Layout, Shell Orientation, Layout again
	layoutProcess(selectedMesh,quickUnwrapperTextureResolution,quickUnwrapperShellPadding,quickUnwrapperTilePadding)
	# If user chose selected edges method, soften/harden edges based on selection; else, skip
	print "ALL DONE!"

def safetyProjection(selectedMesh,quickUnwrapperSafetyProjection):
	# Apply safety UV Projection (Planar Z?)
	cmds.select(selectedMesh+".f[*]")
	facesBuffer = cmds.ls(sl=True,tl=1)
	meshFaces = facesBuffer[0]
	cmds.select(cl=True)
	
	if quickUnwrapperSafetyProjection == 1:
		axis = "x"
	elif quickUnwrapperSafetyProjection == 2:
		axis = "y"
	elif quickUnwrapperSafetyProjection == 3:
		axis = "z"
	else:
		print "What did you do?! I'm defaulting to Z."
		axis = "z"

	cmds.polyProjection(meshFaces,t="Planar",md=axis)
	print "Applied planar projection on axis " + axis

def methodCheck(selectedMesh,selectedEdges,quickUnwrapperMethod,quickUnwrapperAutoAngle,quickUnwrapperAutoSoften):
	# If mesh pre-softened/hardened, skip; if user wants to use selected edges, switch to edge selection; else, apply auto mesh softness based on input (default 45 degrees)
	if quickUnwrapperMethod == 1:
		autoSeamMethod(selectedMesh,quickUnwrapperAutoAngle)
	elif quickUnwrapperMethod == 2:
		softnessMethod(selectedMesh)
	elif quickUnwrapperMethod == 3:
		edgeSelectionMethod(selectedEdges,quickUnwrapperAutoSoften)
	else:
		print "How?! I'm defaulting to Automatic."
		autoSeamMethod(selectedMesh)

def autoSeamMethod(selectedMesh,quickUnwrapperAutoAngle):
	# If user wants to use selected edges, use old method; else, apply auto-seams
	cmds.polySoftEdge(selectedMesh,a=quickUnwrapperAutoAngle)
	print "Auto selected mesh is: " + selectedMesh
	softnessMethod(selectedMesh)
	# polyUVHardEdgesAutoSeams 1 ?

def softnessMethod(selectedMesh):
	# Softness method here if chosen, select and save hard edges, toggle to soft edges and save
	print "Selected Mesh (softness) " + selectedMesh
	cmds.select(selectedMesh)
	cmds.polySelectConstraint(m=3,t=0x8000,sm=1)
	hardEdges = cmds.ls(sl=True)
	cmds.select(selectedMesh+".e[*]",tgl=True)
	softEdges = cmds.ls(sl=True)
	cmds.polySelectConstraint(m=0,sm=0)

	cutSeams(hardEdges)

def edgeSelectionMethod(selectedEdges,quickUnwrapperAutoSoften):
	# If user wants to use selected edges, use old method; else, apply auto-seams
	#selectedEdges = cmds.ls(sl=True)
	hardEdges = selectedEdges
	print "Hard edges: " + hardEdges[0] + hardEdges[1]
	selectionSplit = hardEdges[0].split('.')
	selectedMesh = selectionSplit[0]
	print "Selected mesh: " + selectedMesh
	cmds.select(selectedEdges)
	print "Selected edges: " + selectedEdges[0] + selectedEdges[1]
	cmds.select(selectedMesh+'.e[*]',tgl=True)
	softEdges = cmds.ls(sl=True)
	print "Soft edges: " + softEdges[0]
	cmds.select(cl=True)

	cutSeams(hardEdges)
	
	if quickUnwrapperAutoSoften == 1:
		print "Is Soften/Harden checked? it should be"
		autoSoftenHarden(hardEdges,softEdges);
	else:
		print "Skip, Soften/Harden shouldn't be checked."

def cutSeams(hardEdges):
	# Cut the seams where determined either by the user or by the script, soft edges shouldn't need to be sewn thanks to the safety projection
	print hardEdges
	cmds.polyMapCut(hardEdges)

def unfoldProcess(selectedMesh,quickUnwrapperTextureResolution,quickUnwrapperTilePadding):
	# Apply Unfold3D, then Unfold Legacy step 1 (Horizontal), then Unfold Legacy step 2 (Vertical)
	cmds.u3dUnfold(selectedMesh,ite=1,p=1,bi=1,tf=1,ms=quickUnwrapperTextureResolution,rs=quickUnwrapperTilePadding)
	cmds.unfold(selectedMesh,i=5000,ss=0.001,gb=0,gmb=0.5,pub=False,ps=False,oa=2,us=False)
	cmds.unfold(selectedMesh,i=5000,ss=0.001,gb=0,gmb=0.5,pub=False,ps=False,oa=1,us=False)

def optimizationStep(selectedMesh,quickUnwrapperTextureResolution,quickUnwrapperTilePadding):
	# Apply UV Optimization
	cmds.u3dOptimize(selectedMesh,ite=1,pow=1,sa=1,bi=0,tf=1,ms=quickUnwrapperTextureResolution,rs=quickUnwrapperTilePadding)

def layoutProcess(selectedMesh,quickUnwrapperTextureResolution,quickUnwrapperShellPadding,quickUnwrapperTilePadding):
	# Convert pixel input to UV
	shellPaddingUV = convertPixeltoUV(quickUnwrapperShellPadding)
	tilePaddingUV = convertPixeltoUV(quickUnwrapperShellPadding)
	# Apply Layout step 1, calls for re-orientation of shells, then apply Layout step 2
	cmds.u3dLayout(selectedMesh,res=quickUnwrapperTextureResolution,scl=1,spc=shellPaddingUV,mar=tilePaddingUV,box=[0,1,0,1])
	orientationStep(selectedMesh)
	cmds.u3dLayout(selectedMesh,res=quickUnwrapperTextureResolution,scl=0,spc=shellPaddingUV,mar=tilePaddingUV,box=[0,1,0,1])

def convertPixeltoUV(dataBuffer):
	return dataBuffer*0.0009765625

def orientationStep(selectedMesh):
	# Apply shell Orientation
	# texOrientShells ?
	print "I'm the Shell Orientation function and I'm useless right now..."

def autoSoftenHarden(selectedEdges,unselectedEdges):
	# If user chose selected edges method, soften/harden edges based on selection; else, skip
	cmds.polySoftEdge(selectedEdges,a=0)
	cmds.polySoftEdge(unselectedEdges,a=180)
	
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

	def addButton(self, label, icon="QU_ShelfIcon.png"):
		cmds.setParent(self.shelfName)
		if icon:
			icon = self.iconPath + icon
			cmds.shelfButton(w=32,h=32,i=icon,l=label,mi=("Settings", "python(\"QUTest.checkSavedValues()\");"),c="QUTest.quickRun()",dcc="QUTest.checkSavedValues()",st="iconOnly")

class addShelfIcon(_shelf):
	def build(self):
		self.addButton(label="Quick Unwrapper")