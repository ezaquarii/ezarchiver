#!/usr/bin/env python2

from setuptools import find_packages, setup

# allow setup.py to be run from any path
# os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ezarchiver',
    packages=find_packages(),
    version='1.0.0',
    include_package_data=True,
    package_data={'': ['*/*', '*/*/*', '*/*/*/*', '*/*/*/*/*']},  # nasty hack
    scripts=['scripts/ezbackup', 'scripts/ezrestore'],
    license='GPL-3',
    description='Yet another duplicity wrapper',
    url='https://github.com/ezaquarii/ezarchiver',
    author='Chris Narkiewicz',
    author_email='hello@ezaquarii.com',
    classifiers=[
        'Topic :: System :: Archiving'
        'Topic :: System :: Archiving :: Backup'
    ],
    install_requires=[
        'b2',
        'duplicity >= 0.7.18',
        'pyyaml',
    ],
)
