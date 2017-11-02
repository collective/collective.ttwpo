# -*- coding: utf-8 -*-
"""Installer for the collective.zanata package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='collective.zanata',
    version='1.0a1',
    description="Zanata Translation Service Integration with Plone",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone Translation PO gettext zanata',
    author='Jens W. Klein',
    author_email='jk@kleinundpartner.at',
    url='https://pypi.python.org/pypi/collective.zanata',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'Products.CMFPlone',
        'PyYAML',
        'requests',
        'setuptools',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.testing>=5.0.0',
            'plone.app.contenttypes[test]'
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
