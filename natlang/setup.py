#!/usr/bin/env python

from distutils.core import setup
import nltk

nltk.download('maxent_ne_chunker')
nltk.download('words')

setup(
    name='Bark News',
    version='1.0',
    description='Getting news for dogs',
    author='Matt Lewis',
    author_email='domattthings@gmail.com',
    url='',
    packages=['scraper'],
)
