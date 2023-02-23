from setuptools import setup
import os

setup(
    name = "nanonis_tcp",
    version = "1.0",
    author = "Shixuan Shan, Johannes Schwenk, Clement Soulard",
    author_email = "shixuan.shan@gmail.com",
    description = ("An demonstration of how to create, document, and publish "
                                   "to the cheese shop a5 pypi.org."),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['an_example_pypi_project', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)