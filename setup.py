#!/usr/bin/env python
import os
from django_spark import version
from setuptools import setup

def get_packages():
    # setuptools can't do the job :(
    packages = []
    for root, dirnames, filenames in os.walk('django_spark'):
        if '__init__.py' in filenames:
            packages.append(".".join(os.path.split(root)).strip("."))

    return packages

requires = ['fabric==1.2.0']

setup(name='django-spark',
    version=version,
    description='An app that setups Django apps',
    author=u'Andres Torres Marroquin',
    author_email='andres.torres.marroquin@gmail.com',
    url='https://github.com/Codenga/django-spark',
    packages=get_packages(),
    scripts = ['django_spark/bin/django-spark.py'],
    install_requires=requires,
)