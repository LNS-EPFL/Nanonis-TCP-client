from setuptools import setup
import os

setup(
    name = "nanonis_esr_tcp",
    version = "1.0.1",
    author = "Shixuan Shan, Johannes Schwenk, Clement Soulard ",
    author_email = "shixuan.shan@gmail.com",

    packages = ['nanonis_esr_tcp'],
    url = "https://github.com/LNS-EPFL/Nanonis-TCP-client",
    license = "MIT",
    keywords = "Nanonis, ESR-STM, TCP",
    description = ("A TCP client written in Python which communicates with Nanonis software"),
    # long_description=read('README'),

    classifiers = [
                'Topic :: Scientific/Engineering :: Physics',
                'Operating System :: Microsoft :: Windows :: Windows 10',
                'Operating System :: Microsoft :: Windows :: Windows 11',
                'Intended Audience :: Science/Research',
                'Development Status :: 4 - Beta',
                'License :: OSI Approved :: MIT License',
                'Programming Language :: Python'
                ],
    install_requires = [
    
                        ]
    )