import os
from setuptools import setup, find_packages



setup(
    name="pyotools",
    version=0.1,
    author="Ali Allaoui",
    author_email="ali.allaoui@marsonline.org",
    description=("Collection of tools around pyo and jack"),
    license="GPLv3+",
    packages=find_packages(),
#    long_description=open(os.path.join(os.path.dirname(__file__),
#                                       'README.md')).read(),
    setup_requires=["pyo>=1.0"],
    install_requires=["pyo>=1.0"],
    entry_points={
        'console_scripts': [
        ],
    },

)
