import os

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    author = 'Reece Hart',
    author_email='reecehart+eutils@gmail.com',
    description = """Structured Python interface to NCBI E-Utilities.""",
    license = 'Apache',
    long_description = open('README.rst','r').read(),
    name = "eutils",
    packages = find_packages(),
    url = 'https://bitbucket.org/invitae/eutils',
    use_hg_version = True,
    zip_safe = True,

     classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python",
        "Topic :: Database :: Front-Ends",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        ],

    keywords = [
        'bioinformatics',
        ],
 
    install_requires = [
        'lxml',
        ],

    setup_requires = [
        'hgtools',
        'nose',
        ],    

    tests_require = [
        'coverage',
        'nose',
    ]
)
