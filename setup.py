import setuptools

VERSION = "0.0.1"
DESCRIPTION = "A Python wrapper around the Datagolf API."

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datagolf",
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nscaamano/py-datagolf",
    install_requires=["requests", "pydantic"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
)