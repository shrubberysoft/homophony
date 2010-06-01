from setuptools import setup, find_packages

setup(name='example',
    version='0.1',
    description='Example application for homophony',
    long_description=open('README.md').read(),
    author='Adomas Paltanavicius',
    author_email='adomas.paltanavicius@gmail.com',
    url='http://github.com/shrubberysoft/homophony',
    packages=find_packages('.'),
    install_requires=['homophony']
)
