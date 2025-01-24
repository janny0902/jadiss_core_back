from setuptools import setup, find_packages
import os

def parse_requirements(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()

setup(
    name='jadiss-core-back',
    version='0.1',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
)
