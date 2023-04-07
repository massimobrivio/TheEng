from setuptools import setup, find_packages

VERSION = "1.0"
DESCRIPTION = "General structure optimizer leveraging surrogates."


with open("requirements.txt") as f:
    required = f.read().splitlines()

# Setting up
setup(
    name="theeng",
    version=VERSION,
    author="Massimo Brivio",
    author_email="m.g.brivio@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(where=".", include=["theeng*"]),
    long_description_content_type="text/markdown",
    long_description="TheEng is a Python library for dealing with structural optimization.",
    install_requires=required,
    url="https://github.com/massimobrivio/TheEng",
)

# 1 python setup.py sdist bdist
# 2 twine upload --repository testpypi dist/theeng-1.0.tar.gz
# 3 twine upload dist/theeng-1.0.tar.gz --> only for final release
