from setuptools import setup, find_packages

setup(
    name='jac',
    version='0.1',
    packages=find_packages(exclude=('tests*', )),
    install_requires=open('requirements.txt').read().split('\n')
)
