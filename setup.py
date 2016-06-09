# -*- coding: utf-8 -*-

import io
from setuptools import setup, find_packages


setup(
    name='morepath_wiki',
    version='0.1',
    description=(
        'A wiki demo for Morepath, based on the '
        'web micro-framework battle by Richard Jones'),
    long_description=(
        io.open('README.rst', encoding='utf-8').read() + '\n\n' +
        io.open('CHANGES.rst', encoding='utf-8').read()),
    author='Morepath developers',
    author_email='morepath@googlegroups.com',
    license="BSD",
    url="https://github.com/morepath/morepath_wiki",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords='morepath demo',
    install_requires=[
        'morepath>=0.14,==0.*',
        # 'html', This library has been bundled within the source code.
    ],
    extras_require=dict(
        test=[
            'pytest',
            'pytest-cov',
            'webtest',
        ],
    ),
    entry_points={
        'console_scripts': [
            'morepath_wiki = morepath_wiki.__main__:run',
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
