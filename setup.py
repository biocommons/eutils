from setuptools import setup, find_packages

with open('doc/description-long.txt') as f:
    description_long = f.read()
with open('doc/description-short.txt') as f:
    description_short = f.read()


setup(
    license = 'Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)',
    long_description = description_long,
    description = description_short,
    use_scm_version = True,
    zip_safe = True,

    author = 'Reece Hart',
    author_email='biocommons-dev@googlegroups.com',
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
        'six',
        ],

    setup_requires = [
        'setuptools_scm',
        'sphinx',
        'sphinx_rtd_theme',
        'wheel',
    ],

    tests_require = [
        'pytest',
        'pytest-cov',
        'tox',
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
