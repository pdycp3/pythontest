from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='vector clip by vector',
    ext_modules=cythonize("VectorClipByVector.py"),
)