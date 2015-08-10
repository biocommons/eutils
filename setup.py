from setuptools import setup, find_packages

with open('doc/description.txt') as f:
    long_description = f.read()


setup(
    license = 'Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)',
    long_description = long_description,
    use_scm_version = True,
    zip_safe = True,

    author = 'Reece Hart',
    author_email='reecehart+eutils@gmail.com',
    description = """Structured Python interface to NCBI E-Utilities.""",
    name = "eutils",
    packages = find_packages(),
    url = 'https://bitbucket.org/biocommons/eutils',

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
        'pytz',
        'requests',
        ],

    setup_requires = [
        'setuptools_scm',
        'nose',
        ],

    tests_require = [
        'coverage',
        'nose',
        ],
)

## <LICENSE>
## Copyright 2015 eutils Committers (https://bitbucket.org/biocommons/eutils)
## 
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## 
##     http://www.apache.org/licenses/LICENSE-2.0
## 
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## </LICENSE>
