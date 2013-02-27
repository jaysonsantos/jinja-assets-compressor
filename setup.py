from setuptools import setup, find_packages

setup(
    name='jac',
    author='Jayson Reis',
    author_email='santosdosreis@gmail.com',
    version='0.4',
    packages=find_packages(exclude=('tests*', )),
    install_requires=[
        'beautifulsoup4',
    ],
    description='A Jinja extension (compatible with Flask and other frameworks) to compile and/or compress your assets.'
)
