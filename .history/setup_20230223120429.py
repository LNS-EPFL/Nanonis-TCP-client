from setuptools import setup
import os

setup(
    name = "nanonis_tcp",
    version = "1.0",
    author = "Shixuan Shan, Johannes Schwenk, Clement Soulard ",
    author_email = "shixuan.shan@gmail.com",
    description = ("A TCP client written in Python which communicates with Nanonis software"),
    license = "MIT",
    keywords = "Nanonis, ESR-STM, ",
    url = "",
    packages=['nanonis_tcp'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],)
)