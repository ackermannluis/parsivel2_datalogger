"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="atmscitools",
    version="1.37.0",
    description="Atmospheric Science Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ackermannluis/AtmSciTools",
    author="Luis Ackermann",
    author_email="ackermann.luis@gmail.com",  # Optional
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "License :: OSI Approved :: Apache 2.0",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True,
    package_data={'': ['*.nc','cdsapirc']},
    keywords="weather meteorology instrumentation",
    packages=find_packages(exclude=["contrib", "docs", "tests", "notebooks"]),
    install_requires=["scp", "xlrd", "imageio", "pyproj", "requests", "numpy", "netCDF4", "scipy", "paramiko",
                      "matplotlib", 'Pillow', 'pdf2image'],
    project_urls={"Source": "https://github.com/ackermannluis/AtmSciTools/",},
)
