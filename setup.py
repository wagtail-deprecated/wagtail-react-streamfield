#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from wagtail_react_streamfield import __version__


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(CURRENT_PATH, 'requirements.txt')) as f:
    required = f.read().splitlines()


setup(
    name='wagtail-react-streamfield',
    version=__version__,
    author='NoriPyt',
    author_email='contact@noripyt.com',
    url='https://github.com/noripyt/wagtail-react-streamfield',
    description='The brand new Wagtail StreamField!',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Wagtail :: 2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
    ],
    license='BSD',
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
    zip_safe=False,
)
