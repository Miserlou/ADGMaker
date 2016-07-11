import os
import sys
from setuptools import setup

# Set external files
try:
    from pypandoc import convert
    README = convert('README.md', 'rst')     
except ImportError:
    README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()

setup(
    name='adgmaker',
    version='0.1.3',
    packages=['adgmaker'],
    install_requires=required,
    test_suite='nose.collector',
    include_package_data=True,
    license='MIT License',
    description='Create Free Ableton Live Instruments from Philharmonic Samples',
    long_description=README,
    url='https://github.com/Miserlou/ADGMaker',
    author='Rich Jones',
    author_email='rich@openwatch.net',
    entry_points={
        'console_scripts': [
            'adgmaker=adgmaker.adgmaker:handle',
        ]
    },
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
