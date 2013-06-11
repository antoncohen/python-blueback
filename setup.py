try:
    from setuptool import setup
except ImportError:
    from ditutils.core import setup

name = 'python-blueback'
version = '0.1'
packages = ['python-blueback']
description='Cloud backup utility'
requires = []

setup(
    name=name,
    description=description,
    version=version,
    author='Anton Cohen',
    author_email='anton@antoncohen.com',
    url='https://github.com/antoncohen' + name,
    packages=packages,
    install_requires=requires,
    scripts=[]
)


