import sys

from os.path import join, abspath, dirname
from setuptools import setup

CWD = abspath(dirname(__file__))

try:
    import redisblog
except ImportError:
    sys.path.insert(0, CWD)
    import redisblog


def install_requires():
    with open(join(CWD, 'requirements.txt'), 'r') as f:
        reqs = [one for one in f.readlines() if one and not one.startswith('#')]

    base = ['setuptools>=0.6b1']
    return base + reqs

tests_require = [
    'nose',
    'coverage',
]

with open('README.rst') as readmefile:
    long_description = readmefile.read()


setup(
    name='bottle-redisblog',
    version=redisblog.__versionstr__,
    description='Bottle redisblog is blog ',
    long_description=long_description,
    author='Michal Dub',
    author_email='michalmam@centrum.cz',
    maintainer='Michal Dub',
    maintainer_email='michalmam@centrum.cz',
    license='BSD',
    url='https://github.com/MichalMaM/bottle-redisblog',

    packages=('redisblog', 'core', 'articles'),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Framework :: Bottle",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires=install_requires(),
    test_suite='nose.collector',
    tests_require=tests_require
)
