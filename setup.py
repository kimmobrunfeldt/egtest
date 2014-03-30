#!/usr/bin/env python

from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

print(reqs)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = """Read docs from GitHub_

.. _GitHub: https://github.com/kimmobrunfeldt/egtest
"""

setup(
    name='egtest',
    version='0.1.0',
    description='Test example code blocks in documentation',
    long_description=readme,
    author='Kimmo Brunfeldt',
    author_email='kimmobrunfeldt@gmail.com',
    url='https://github.com/kimmobrunfeldt/egtest',
    packages=[
        'egtest',
    ],
    entry_points={
        'console_scripts': [
            'egtest = egtest.main:main'
        ],
    },
    package_dir={'egtest': 'egtest'},
    include_package_data=True,
    install_requires=reqs,
    dependency_links=['https://github.com/kimmobrunfeldt/colorama/tarball/master#egg=colorama'],
    license='MIT',
    zip_safe=False,
    keywords='egtest test documentation doctest',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
