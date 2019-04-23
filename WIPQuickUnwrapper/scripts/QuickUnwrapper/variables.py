import maya.cmds as cmds

def check():
	if "QU_SafetyProjectionAxis" not in cmds.env.optionVars: cmds.optionVar(iv=("QU_SafetyProjectionAxis",3))
	if "QU_Method" not in cmds.env.optionVars: cmds.optionVar(iv=("QU_Method",1))
	if "QU_AutoAngle" not in cmds.env.optionVars: cmds.optionVar(fv=("QU_AutoAngle",60.00))
	if "QU_AutoSoften" not in cmds.env.optionVars: cmds.optionVar(iv=("QU_AutoSoften",0))
	if "QU_TextureResolution" not in cmds.env.optionVars: cmds.optionVar(iv=("QU_TextureResolution",3))
	if "QU_TexelDensity" not in cmds.env.optionVars: cmds.optionVar(fv=("QU_TexelDensity",20.48))
	if "QU_ShellPadding" not in cmds.env.optionVars: cmds.optionVar(iv=("QU_ShellPadding",4))
	if "QU_TilePadding" not in cmds.env.optionVars: cmds.optionVar(iv=("QU_TilePadding",8))
	if "QU_StackSimilarShells" not in cmds.env.optionVars: cmds.optionVar(iv=("QU_StackSimilarShells",0))