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