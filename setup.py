#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='drivendata-submission-validator',
    version='1.0.0',
    description='DrivenData Submission Validator',
    author='DrivenData, Inc.',
    author_email='info@drivendata.org',
    url='http://www.drivendata.org/',
    license='MIT',
    packages=find_packages(exclude=['examples']),

    entry_points={
    'console_scripts': [
        'dd-sub-valid=drivendata_validator.drivendata_validator:main',
    ]},
    
    install_requires=[
        "pandas>=0.13", 
        "numpy>=1.7",
    ],

    zip_safe=True,
)