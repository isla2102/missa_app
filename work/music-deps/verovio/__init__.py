"""""" # start delvewheel patch
def _delvewheel_patch_1_13_0():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'verovio.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_13_0()
del _delvewheel_patch_1_13_0
# end delvewheel patch

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

from .verovio import *

verovio.setDefaultResourcePath(str(files("verovio") / "data"))
