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
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Wagtail :: 2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    license='BSD',
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
    zip_safe=False,
)
