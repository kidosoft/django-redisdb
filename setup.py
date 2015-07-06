from setuptools import setup, find_packages

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='django-redisdb',
    version='0.2.1',
    description='Django redis backend',
    long_description=long_description,
    url='http://django-redisdb.readthedocs.org',
    author='Jakub STOLARSKI (Dryobates)',
    author_email='jakub.stolarski@kidosoft.pl',
    license='beerware',
    keywords='django redis',
    packages=find_packages('src', exclude=['example*', '*.tests', 'tests.*', '*.tests.*', 'tests']),
    package_dir={'': 'src'},
    install_requires=[
        'redis',
        'hash_ring',
        'Django>=1.2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite="redisdb.tests",
)
