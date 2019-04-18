Quick Unwrapper v1.1 Known Issues

General:
	• Large meshes (high poly count) can cause the script to throw an error and/or crash.
	• The safety planar UV projection can, in some cases, "break" the UVs and prevent the script from properly unwrapping
		(e.g. running an X-axis or Z-axis safety planar projection on a Y-axis facing cylinder will make the caps' UVs a perfectly flat line and prevent maya from unfolding them)
	• Using the Automatic method on certain shapes, such as cylinders or spheres, will not unwrap the UVs properly as it won't know that the surface of the cylinder also needs to be cut.
	• The succession of unfolds (u3dUnfold + legacy Unfold) does not unfold certain UV shells as expected and as it would if the user were to manually go through the same steps as the script.
		(e.g. when running the script on a cylinder, the surface of the cylinder's UVs will be inflated)
	• Print helpers remain present in the script and will print relevant information as the script is processing the user's requests.
	• Missing some safety measures to keep track of the user's selected mesh, resulting in an error if the user selects their mesh in any other way than the expected one.
		(e.g. when running the script using the Automatic method on a mesh that is selected in Vertex/Edge/Face mode, the script won't properly save the mesh's name and will attempt to unwrap nothing)

Shelf Button:
	• Missing shelf icon, Maya will generate the button using a blank bracketed icon.
	• Quick run (single click on shelf button) does nothing as of yet (Full run by double clicking the shelf button or right clicking and selecting the Settings option does work).

Functionality:
	• Shell Stacking option appears to have broken.
	• Pixel Density option is currently only a UI component and has no function.
	• Shell Orientation is currently skipped as its function contains no code.