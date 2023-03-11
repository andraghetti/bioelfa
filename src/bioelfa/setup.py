#!/usr/bin/env python3

"""package setup"""

from setuptools import find_namespace_packages, setup

REQUIREMENTS = [
    'tqdm',
    'pandas',
    'biopython',
    'numpy',
    'rich_click'
]

CONSOLE_SCRIPTS = [
    'normalize=normalizer:normalize',
    'genecompare=geneset_compare:main',
]

setup(
    name='bioelfa',
    packages=find_namespace_packages(exclude=['data']),
    version='0.1.1',
    author='Lorenzo Andraghetti',
    author_email='andraghetti.l@gmail.com',
    maintainer_email='andraghetti.l@gmail.com',
    license='MIT',
    platforms=['any'],
    install_requires=REQUIREMENTS,
    python_requires='>=3.8.0',
    entry_points={'console_scripts': CONSOLE_SCRIPTS},
)
