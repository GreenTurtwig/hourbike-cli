from setuptools import setup

setup(
    name="hourbike-cli",
    version="1.0",
    description="A CLI for Hourbike schemes across the UK",
    long_description=open("README.rst").read(),
    url="https://github.com/GreenTurtwig/hourbike-cli",
    author="GreenTurtwig",
    license="MIT",
    py_modules=["hourbike"],
    install_requires=[
        "click",
        "requests",
        "geopy"
    ],
    entry_points={
        "console_scripts": ["hourbike=hourbike:run"]
    },
    keywords="cli bike bicycle hire",
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Topic :: Utilities"
    ]
)