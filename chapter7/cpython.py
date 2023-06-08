import os 
from distutils.core import setup
from distutils.extension import Extension

try:
    # cpython source tp source compilation available 
    # only when cpython is avaiable 
    import Cpython 
    # and specific enviroment variable says
    # explicitely that cpython should be used to generate c sources 
    USE_CYTHON = bool(os.environ.get('USE_CTRHON'))
except ImportError:
    USE_CYTHON = False

ext = '.pyx' if USE_CYTHON else '.c'
extensions = [Extension('fibonacci',['fibonacci'+ext])]

if USE_CYTHON:
    from Cython.Build import cythonize 
    extensions = cythonize(extensions)

setup(
    name = 'fibonacci',
    ext_modules=extensions,
    extras_require = {
        # Cython will be set in that specific version
        # as a requirement if package will be intalled
        # with '[with-cython]' extra feature
        "cpython":['cython==0.23.4']
    }
)