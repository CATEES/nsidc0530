from distutils.core import setup

import yaml

with open('meta.yaml', 'r') as f:
    doc = yaml.load(f)

version = doc['package']['version']
name = doc['package']['name']
    
setup(
    name=name,
    version=version,
    packages=[name],
    package_data={name: ['latlon.gz']},
    author='Paul Madden',
    author_email='pmadden@nsidc.org',
    url='https://github.com/catees/%s' % name,
)
