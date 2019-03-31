import maya.cmds as cmds

'''
import QuickUnwrapper
reload(QuickUnwrapper)
QuickUnwrapper.quWindow()
'''

def quWindow(setProjAxis,setMethod,setAngle,setSoftness,setResolution,setShellPad,setTilePad,setShellStack):
	if cmds.window("quWindow",ex=True):
		cmds.deleteUI("quWindow",wnd=True)
	if cmds.windowPref("quwindow",ex=True):
		cmds.windowPref("quWindow",r=True)

	cmds.window("quWindow",t="Quick Unwrapper",w=128,h=128,rtf=True,mnb=True,mxb=False,s=False)

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
	automaticAngle = cmds.floatField(v=setAngle,min=15.0,max=90.0,w=40,pre=2)
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
	cmds.button(l="Unwrap",w=64,h=32,ann="Process the request and unwrap selected mesh.",c=(lambda args: checkVars(safetyProjectionAxis,methodSelect,automaticAngle,autoSoften,layoutResolution,shellPadding,tilePadding,stackSimilar)))
	cmds.button(l="Cancel",w=64,h=32,ann="Cancel and close script.",c=("cmds.deleteUI(\"quWindow\",wnd=True); cmds.windowPref(\"quWindow\",r=True)"))
	cmds.separator(w=256,h=8,st="none",p="quContainer")

	cmds.showWindow("quWindow")

def processRequest():
	# Save current selection
	selectionBuffer = cmds.ls(sl=True,tr=True,tl=1,sn=True)
	selectedMesh = selectionBuffer[0]
	# Apply safety UV Projection (Planar Z?)
	safetyProjection(selectedMesh)
	# If mesh pre-softened/hardened, skip; if user wants to use selected edges, switch to edge selection; else, apply auto mesh softness based on input (default 45 degrees)
	methodCheck()
	# Apply Unfold3D
	unfoldProcess()
	# Apply UV Optimization
	optimizationStep()
	# Apply Layout
	layoutProcess()
	# Apply shell Orientation
	# Apply Layout step 2
	# If user chose selected edges method, soften/harden edges based on selection; else, skip

def safetyProjection(selectedMesh):
	# Apply safety UV Projection (Planar Z?)
	cmds.select(selectedMesh+".f[*]")
	facesBuffer = cmds.ls(sl=True,tl=1)
	meshFaces = facesBuffer[0]
	cmds.select(cl=True)

	cmds.polyProjection(meshFaces,t="Planar",md="z")

def methodCheck():
	# If mesh pre-softened/hardened, skip; if user wants to use selected edges, switch to edge selection; else, apply auto mesh softness based on input (default 45 degrees)
	# autoSeamMethod(selectedMesh)
	# softnessMethod(selectedMesh)
	# edgeSelectionMethod()
	print "poot"

def autoSeamMethod(selectedMesh):
	# If user wants to use selected edges, use old method; else, apply auto-seams
	cmds.polySoftEdge(selectedMesh,a=60)
	# polyUVHardEdgesAutoSeams 1 ?
	cutSeams()

def softnessMethod(selectedMesh):
	# Softness method here if chosen, select and save hard edges, toggle to soft edges and save
	cmds.polySelectConstraint(m=3,t=0x8000,sm=1)
	hardEdges = cmds.ls(sl=True)
	cmds.select(selectedMesh[0]+".e[*]",tgl=True)
	softEdges = cmds.ls(sl=True)
	cmds.polySelectConstraint(m=0,sm=0)

	cutSeams()

def edgeSelectionMethod():
	# If user wants to use selected edges, use old method; else, apply auto-seams
	selectedEdges = cmds.ls(sl=True)
	hardEdges = selectedEdges[0]
	selectionSplit = hardEdges.split('.')
	selectedMesh = selectionSplit[0]
	cmds.select(selectedMesh+'.e[*]',tgl=True)
	softEdges = cmds.ls(sl=True)
	cmds.select(cl=True)

	cutSeams(hardEdges)
	autoSoftenHarden(hardEdges,softEdges);

def cutSeams(hardEdges):
	# Cut the seams where determined either by the user of by the script
	polyMapCut(hardEdges)

def unfoldProcess():
	# Apply Unfold3D, then Unfold Legacy step 1 (Horizontal), then Unfold Legacy step 2 (Vertical)
	cmds.u3dUnfold(selectedMesh,ite=1,p=1,bi=1,tf=1,ms=layoutResolution,rs=16)
	cmds.unfold(selectedMesh,i=5000,ss=0.001,gb=0,gmb=0.5,pub=False,pa=False,oa=2,us=False)
	cmds.unfold(selectedMesh,i=5000,ss=0.001,gb=0,gmb=0.5,pub=False,ps=False,oa=1,us=False)

def optimizationStep():
	# Apply UV Optimization
	cmds.u3dOptimize(selectedMesh,ite=1,pow=1,sa=1,bi=0,tf=1,ms=layoutResolution,rs=0)

def layoutProcess():
	# Apply Layout step 1, calls for re-orientation of shells, then apply Layout step 2
	cmds.u3dLayout(selectedMesh,res=1024,scl=1,spc=0.001953125,mar=0.00390625,box=[0,1,0,1])
	orientationStep(selectedMesh)
	cmds.u3dLayout(selectedMesh,res=1024,scl=0,spc=0.001953125,mar=0.00390625,box=[0,1,0,1])

def orientationStep():
	# Apply shell Orientation
	# texOrientShells ?
	print "burp"

def autoSoftenHarden(selectedEdges,unselectedEdges):
	# If user chose selected edges method, soften/harden edges based on selection; else, skip
	cmds.polySoftEdge(selectedEdges,a=0)
	cmds.polySoftEdge(unselectedEdges,a=180)

# def makeShelfButton():
	# Call QUShelf.py to generate shelf icon in the Poly Modeling tab

quWindow()