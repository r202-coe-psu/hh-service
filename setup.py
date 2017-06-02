'''
HH-service
----------

A service core for HomeHero
'''

import re
import ast
from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('hhservice/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
            f.read().decode('utf-8')).group(1)))
setup(
    name='hhservice',
    version=version,
    url='',
    license='',
    author='',
    author_email='',
    description='A service core for HomeHero',
    long_description=__doc__,
    packages=['hhservice'],
    include_package_data=True,
    install_requires=[
        'flask',
        'jinja2',
        'flask-login',
        'flask-principal',
        'flask-wtf',
        'flask-restful'
    ],
     dependency_links =[
         'https://github.com/sdayu/rethinkengine.git'
    ],
    classifiers=[
    ],
    entry_points='''
        [console_scripts]
        hhservice-web=hhservice.cmd.web:main
        hhservice-api=hhservice.cmd.api:main
    '''
)

