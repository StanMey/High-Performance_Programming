from setuptools import setup
from Cython.Build import cythonize

import numpy

setup(
    ext_modules = cythonize('seq_sieve.pyx',
                            annotate=True,
                            language_level="3"),
    include_dirs=[numpy.get_include()],
    zip_safe=False
    )
