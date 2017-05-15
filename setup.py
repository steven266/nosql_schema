from setuptools import setup, find_packages

setup(
    name='nosql_schema',
    version='0.2.4',
    description='A simple object document mapper for nosqlite',
    url='https://github.com/steven266/nosql_schema',
    author='Steven Cardoso',
    author_email='hello@steven266.de',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='odm nosqlite sqlite flask',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[],
)
