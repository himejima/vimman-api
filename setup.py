from setuptools import find_packages
from setuptools import setup
import sys

sys.path.append('./src')
sys.path.append('./tests')

setup(
    name='vimman-api',
    version='0.1',
    description='This is test codes for travis ci',
    packages=find_packages(),
    test_suite='run.suite'
)
