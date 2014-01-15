
from setuptools import setup, find_packages

setup(
    name = "eutils",
    description = """Structured Python interface to NCBI E-Utilities.""",
    license = 'MIT',
    version = "0.0.0",
    author_email='reecehart@gmail.com',
    packages = find_packages(),
    zip_safe = True,
    #test_suite = 'nose.collector',
    install_requires = [
        'lxml',
        'nose',
        ],    
)
