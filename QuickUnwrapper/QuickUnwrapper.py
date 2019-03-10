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

	cmds.window("quWindow",t="Quick Unwrapper",rtf=True,mnb=False,mxb=False,s=True)
	cmds.columnLayout("quContainer",cat=("both",10),cw=200,p="quWindow")
	cmds.rowLayout("shelfOffer")
	cmds.button(ann="Add QuickUnwrapper to the current shelf",l="Add to shelf",w=180,h=20,c=(lambda _: makeShelfButton()))
	cmds.setParent("quContainer")
	cmds.separator(w=180,h=10,st="none")
	cmds.rowLayout("dropSeam",nc=2)
	cmds.text(l="Seams at ")
	seamSet = cmds.optionMenu(p="dropSeam")
	cmds.menuItem(l="Selected Edges")
	cmds.menuItem(l="Hard Edges")
	cmds.setParent("quContainer")
	cmds.rowLayout("dropReso",nc=2)
	cmds.text(l="Resolution ")
	resoSet = cmds.optionMenu(p="dropReso")
	cmds.menuItem(l="2048")
	cmds.menuItem(l="1024")
	cmds.setParent("quContainer")
	cmds.separator(w=180,h=10,st="none")
	autoSoft = cmds.checkBox(l=" Automatic Soften")
	cmds.separator(w=180,h=4,st="none")
	fitTex = cmds.checkBox(l=" Fit Texel Density")
	cmds.separator(w=180,h=4,st="none")
	autoLay = cmds.checkBox(l=" Automatic Layout")
	cmds.separator(w=180,h=10,st="none")
	cmds.rowLayout(nc=2,p="quContainer")
	cmds.button(l="Unwrap",w=90,h=30,c=(lambda _: runUnwrap()))
	cmds.button(l="Cancel",w=90,h=30,c=("cmds.deleteUI(\"quWindow\",window=True)"))
	cmds.setParent("quContainer")

	cmds.showWindow("quWindow")

def makeShelfButton():
	shelfIcon = "QU_shelfIcon.png"
	mayaShelf = mmel.eval("$temp = $gShelfTopLevel")
	currentShelf = cmds.tabLayout(mayaShelf,q=True,st=True)
	shelfLocation = mayaShelf + "|" + currentShelf
	cmds.shelfButton(ann="Quick Unwrap",c=(lambda : runUnwrap()),dcc=(lambda : quWindow()),h=34,w=34,i=shelfIcon,mi=("Auto Smooth", "python(\"import QUAutoSmooth\");" "python(\"reload(QUAutoSmooth)\");"),l="Quick Unwrap",p=shelfLocation,stp="python",st="iconOnly")

def runUnwrap():
	selectedEdges = cmds.ls(sl=True)
	selectionBuffer = selectedEdges[0]
	selectionSplit = selectionBuffer.split('.')
	selectedMesh = selectionSplit[0]
	cmds.select(selectedMesh+'.e[*]',tgl=True)
	unselectedEdges = cmds.ls(sl=True)
	cmds.select(cl=True)
	cmds.polyMapSew(unselectedEdges)
	cmds.polyMapCut(selectedEdges)
	cmds.u3dUnfold(selectedMesh,ite=1,p=1,bi=1,tf=1,ms=2048,rs=16)
	cmds.u3dLayout(selectedMesh,res=2048,rot=5,scl=1,spc=0.0078125,mar=0.00390625,box=(0,1,0,1))

def autoSmooth():
	selectedMesh = cmds.ls(sl=True)
	cmds.select(selectedMesh[0]+".map[*]")
	allUV = cmds.ls(sl=True)
	selHarden = cmds.polySelectConstraint(uv=1,bo=0,m=2,rs=1)
	cmds.select(selHarden[0])
	selHarden = cmds.polySelectConstraint(t=0x0010,uv=0,bo=1,m=2,rs=1)
	cmds.select(selHarden)
	selHarden = cmds.polyListComponentConversion(fuv=True,te=True,internal=True)
	cmds.select(selHarden)
	selSoften = cmds.select(selectedMesh[0]+".e[*]",tgl=True)
	selSoften = cmds.ls(sl=True)
	cmds.polySoftEdge(selSoften,a=180,ch=False)
	cmds.polySoftEdge(selHarden,a=0,ch=False)
	cmds.polySelectConstraint(dis=True)

quWindow()