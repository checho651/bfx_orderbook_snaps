"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
setup(
    name='bfx_orderbook_snaps',
    version='1.0.2',
    description='bfx ordebook snaps',
    long_description='Store orderbook snapshots from bitfinex',
    long_description_content_type='text/markdown',
    url='https://github.com/checho651/bfx_orderbook_snaps',
    author='Checho',
    author_email='maquieiraezequiel@gmail.com ',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Project Audience
        'Intended Audience :: Internal',
        'Topic :: Software Development :: Build Tools',
        # Project License
        'License :: OSI Approved :: Apache Software License',

        # Python versions (not enforced)
        'Programming Language :: Python :: 3.8',
    ],
    keywords='bitfinex,api,trading',
    packages=find_packages(exclude=['examples', 'tests', 'docs']),
    # Python versions (enforced)
    python_requires='>=3.8.0, <4',
    # deps installed by pip
    install_requires=['requests', 'schedule'],
    project_urls={
        'Bug Reports': 'https://github.com/checho651/bfx_orderbook_snaps/issues',
        'Source': 'https://github.com/checho651/bfx_orderbook_snaps',
    },
)
