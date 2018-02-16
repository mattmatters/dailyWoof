"""Scraper Setup"""

from setuptools import setup
# from distutils.core import setup

setup(
    name='Bark News Scraper',
    version='1.0',
    description='Getting news for dogs',
    author='Matt Lewis',
    author_email='domattthings@gmail.com',
    url='',
    packages=['scraper'],
    install_requires=[
        'selenium',
        'redis',
        'pika',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pylint',
    ],
)
