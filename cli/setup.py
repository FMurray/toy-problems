
from setuptools import setup, find_packages
from toy-problems.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='toy-problems',
    version=VERSION,
    description='A collection of tools for practicing data structures and algorithms toy problems.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Forrest Murray',
    author_email='fmurray@gmail.com',
    url='https://github.com/fmurray/toy-projects',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'toy-problems': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        toy-problems = toy-problems.main:main
    """,
)
