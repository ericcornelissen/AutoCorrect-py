# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name='AutoCorrect',
    version='0.2.0',
    description='A simple self-learning dictionary to autocorrect texts',
    long_description=readme,
    author='Eric Cornelissen',
    author_email='ericornelissen@gmail.com',
    url='https://github.com/ericcornelissen/AutoCorrect-py',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
