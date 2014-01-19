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
    url = 'https://bitbucket.org/reece/rcore',
    use_hg_version = True,
    zip_safe = True,

    classifiers = [
        "License :: OSI Approved :: MIT License",
        ],

    keywords = [
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
