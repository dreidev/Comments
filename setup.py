# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-ajax-comments',
    version='1.0.8.dev1',
    author=u'DREIDEV',
    author_email='info@dreidev.com',
    url='https://github.com/dreidev/Comments',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

         'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='comments comment development',
    description='Associates comments functionality with any given model',
    zip_safe=False,
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
)
