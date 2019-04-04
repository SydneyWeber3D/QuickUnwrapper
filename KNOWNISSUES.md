Quick Unwrapper KNOWN ISSUES

- Large meshes (high poly count) can cause the script to throw an error
- Using the automatic method on certain shapes (such as cylinders) will not unwrap UVs properly (as it won't know that the surface of the cylinder also needs to be cut)
- The succession of unfolds (u3dUnfold + legacy Unfold) does not unfold certain UV shells as expected (and as it would if the user were to manually go through the same steps as the script)