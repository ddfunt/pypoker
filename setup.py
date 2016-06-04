#!/usr/bin/env python
"""

Copyright 2015 BrightSpec
"""

import os
import re
import sys

from setuptools import setup, find_packages


classifiers = [
    'Development Status :: 1 - Planning',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
]

from pip.req import parse_requirements
from pip.download import PipSession
install_reqs = parse_requirements('requirements.txt', session=PipSession())

install_requires = [str(req.req) for req in install_reqs]

lint_requires = [
    'flake8',
]

tests_require = [
    'mock',
    'pytest',
]

dependency_links = []

setup_requires = []


def get_version(filepath='Edgar/_version_generated.py'):
    """Get version without import, which avoids dependency issues."""
    pass


def readme(filepath='README.md'):
    """Return project README.rst contents as str."""
    with open(get_abspath(filepath)) as fd:
        return fd.read()


def description(doc=__doc__):
    """Return project description from first line of doc."""
    for line in doc.splitlines():
        return line.strip()


def get_abspath(filepath):
    if os.path.isabs(filepath):
        return filepath
    setup_py = os.path.abspath(__file__)
    project_dir = os.path.dirname(setup_py)
    return os.path.abspath(os.path.join(project_dir, filepath))


packages = find_packages(include=["poker*"])


setup(
    name='poker',
    version=get_version(),
    author='Matt',
    author_email='diracdeltafunct@gmail.com',
    url='spectralengine.com',
    description=description(),
    long_description=readme(),
    packages=packages,
    entry_points={
        'console_scripts': [
        ]
    },
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    extras_require={
        'test': tests_require,
        'all': install_requires + tests_require,
        'lint': lint_requires
    },
    dependency_links=dependency_links,
    zip_safe=False,
    test_suite='nose.collector',
    include_package_data=True,
)

