import maya.cmds as cmds

def check():
	if cmds.optionVar(ex="QU_SafetyProjectionAxis"):
		pass
	else:
		cmds.optionVar(iv=("QU_SafetyProjectionAxis",4))
	if cmds.optionVar(ex="QU_Method"):
		pass
	else:
		cmds.optionVar(iv=("QU_Method",1))
	if cmds.optionVar(ex="QU_AutoAngle"):
		pass
	else:
		cmds.optionVar(fv=("QU_AutoAngle",60.00))
	if cmds.optionVar(ex="QU_AutoSoften"):
		pass
	else:
		cmds.optionVar(sv=("QU_AutoSoften","True"))
	if cmds.optionVar(ex="QU_TextureResolutionID"):
		pass
	else:
		cmds.optionVar(iv=("QU_TextureResolutionID",3))
	if cmds.optionVar(ex="QU_TextureResolution"):
		pass
	else:
		cmds.optionVar(iv=("QU_TextureResolution",2048))
	if cmds.optionVar(ex="QU_ShellPadding"):
		pass
	else:
		cmds.optionVar(iv=("QU_ShellPadding",4))
	if cmds.optionVar(ex="QU_TilePadding"):
		pass
	else:
		cmds.optionVar(iv=("QU_TilePadding",8))