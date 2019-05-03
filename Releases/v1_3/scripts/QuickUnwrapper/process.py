import maya.cmds as cmds

#	Process user's unwrapping request based on their input.
def processRequest():
	selectedMesh, selectedEdges = selectionFilter()
	
	safetyProjection(selectedMesh)
	
	methodCheck(selectedMesh,selectedEdges)
	
	unfoldProcess(selectedMesh)
	
	optimizationStep(selectedMesh)
	
	layoutProcess(selectedMesh)
	
	cmds.select(selectedMesh)

#	Filter user selection to prevent errors.
def selectionFilter():
	userSelection = cmds.ls(sl=True)
	userHighlight = cmds.ls(hl=True)
	
	if not userSelection:
		return userHighlight[0], None
	else:
		if ".e[" in userSelection[0]:
			return userHighlight[0], userSelection
		elif '.' in userSelection[0]:
			return userHighlight[0], None
		else:
			return userSelection[0], None

#	Apply safety UV projection.
def safetyProjection(selectedMesh):
	cmds.select(selectedMesh+".f[*]")
	meshFaces = cmds.ls(sl=True,tl=1)[0]
	cmds.select(cl=True)
	
	if cmds.optionVar(q="QU_SafetyProjectionAxis") == 1:
		axis = 'x'
	elif cmds.optionVar(q="QU_SafetyProjectionAxis") == 2:
		axis = 'y'
	elif cmds.optionVar(q="QU_SafetyProjectionAxis") == 3:
		axis = 'z'
	elif cmds.optionVar(q="QU_SafetyProjectionAxis") == 4:
		axis = 'p'
	
	cmds.polyProjection(meshFaces,t="Planar",md=axis)

#	Check for user chosen unwrapping method.
def methodCheck(selectedMesh,selectedEdges):
	if cmds.optionVar(q="QU_Method") == 1:
		autoSeamMethod(selectedMesh)
	elif cmds.optionVar(q="QU_Method") == 2:
		softnessMethod(selectedMesh)
	elif cmds.optionVar(q="QU_Method") == 3:
		edgeSelectionMethod(selectedMesh,selectedEdges)
	else:
		print "Incorrect method value, defaulting to Automatic."
		autoSeamMethod(selectedMesh)

#	Automatic unwrap method here.
def autoSeamMethod(selectedMesh):
	cmds.polySoftEdge(selectedMesh,a=cmds.optionVar(q="QU_AutoAngle"))
	softnessMethod(selectedMesh)

#	Softness based unwrap method here.
def softnessMethod(selectedMesh):
	cmds.select(selectedMesh)
	cmds.polySelectConstraint(m=3,t=0x8000,sm=1)
	hardEdges = cmds.ls(sl=True)
	cmds.polySelectConstraint(m=0,sm=0)
	edgeSelectionMethod(selectedMesh,hardEdges)
	
#	Edge selection based unwrap method here.
def edgeSelectionMethod(selectedMesh,selectedEdges):
	cmds.polyMapCut(selectedEdges)
	cmds.select(selectedEdges)
	cmds.select(selectedMesh+".e[*]",tgl=True)
	remainingEdges = cmds.ls(sl=True)
	
	if cmds.optionVar(q="QU_AutoSoften") == "True":
		autoSoftenHarden(selectedEdges,remainingEdges)

#	Apply Unfold3D, then polish results by re-unfolding twice with vertical then horizontal constraints.
def unfoldProcess(selectedMesh):
	cmds.u3dUnfold(selectedMesh,ite=1,p=1,bi=1,tf=1,ms=cmds.optionVar(q="QU_TextureResolution"),rs=cmds.optionVar(q="QU_TilePadding"))
	cmds.unfold(selectedMesh,i=5000,ss=0.001,gb=0,gmb=0.5,pub=False,ps=False,oa=1,us=False)
	cmds.unfold(selectedMesh,i=5000,ss=0.001,gb=0,gmb=0.5,pub=False,ps=False,oa=2,us=False)

#	Optimize UVs.
def optimizationStep(selectedMesh):
	cmds.u3dOptimize(selectedMesh,ite=1,pow=1,sa=1,bi=0,tf=1,ms=cmds.optionVar(q="QU_TextureResolution"),rs=cmds.optionVar(q="QU_TilePadding"))

#	Apply UV Layout, call for re-orientation of shells, then re-apply UV Layout for tighter packing.
def layoutProcess(selectedMesh):
	shellPadding = convertPixeltoUV(cmds.optionVar(q="QU_ShellPadding"))
	tilePadding = convertPixeltoUV(cmds.optionVar(q="QU_TilePadding"))
	
	cmds.u3dLayout(selectedMesh,res=cmds.optionVar(q="QU_TextureResolution"),scl=1,spc=shellPadding,mar=tilePadding,box=[0,1,0,1])
	orientationStep(selectedMesh)
	cmds.u3dLayout(selectedMesh,res=cmds.optionVar(q="QU_TextureResolution"),scl=0,spc=shellPadding,mar=tilePadding,box=[0,1,0,1])

#	Convert pixel spacing to UV spacing.
def convertPixeltoUV(dataBuffer):
	return dataBuffer*0.0009765625

#	Re-orient shells so that they take the least amount of space.
def orientationStep(selectedMesh):
	cmds.polyLayoutUV(selectedMesh,fr=False,l=0,lm=1,ps=0.2,rbf=3,sc=0,se=0)

#	Soften or Harden the mesh's edges to match UV borders for potential baking.
def autoSoftenHarden(selectedEdges,remainingEdges):
	cmds.polySoftEdge(selectedEdges,a=0)
	cmds.polySoftEdge(remainingEdges,a=180)