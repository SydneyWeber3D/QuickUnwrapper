Quick Unwrapper v1.2 Known Issues

General:
	• Large meshes (high poly count) can cause the script to throw an error and/or crash.
	• The safety planar UV projection can, in some cases, "break" the UVs and prevent the script from properly unwrapping.
		(e.g. running an X-axis or Z-axis safety planar projection on a Y-axis facing cylinder will make the caps' UVs a perfectly flat line and prevent maya from unfolding them)
	• Using the Automatic method on certain shapes, such as cylinders or spheres, will not unwrap the UVs properly as it won't know that the surface of the cylinder also needs to be cut.
	• The succession of unfolds (u3dUnfold + legacy Unfold) does not unfold certain UV shells as expected and as it would if the user were to manually go through the same steps as the script.
		(e.g. when running the script on a cylinder, the surface of the cylinder's UVs will be inflated)

Functionality:
	• Shell Stacking option is currently only a UI component and has no function.
	• Texel Density option is currently only a UI component and has no function.
	• Shell Orientation option is currently only a UI component and has no function.