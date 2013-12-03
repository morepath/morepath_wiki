import os
from setuptools import setup, find_packages

setup(name='mpwiki',
      version = '0.1dev',
      description="Morepath Wiki inspired by web-micro-battle",
      author="Martijn Faassen",
      author_email="faassen@startifact.com",
      license="BSD",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'morepath',
        'html',
        ],
      entry_points= {
        'console_scripts': [
            'morepath_wiki = mpwiki.wiki:main',
            ]
        },
      )
