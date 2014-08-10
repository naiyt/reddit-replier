from setuptools import setup, find_packages
from codecs import open
from os import path
import sys

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

required = ['praw']
if sys.version_info <= (3,2):
    required.append('mock')

setup(
    name='redditreplier',
    version='1.0.1rc1',
    description='Create Reddit Bots',
    long_description=long_description,
    url='https://github.com/naiyt/reddit-replier',
    author='Nate Collings',
    author_email='nate@natecollings.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='reddit bots automation praw',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=required
)
