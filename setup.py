import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bearer",
    version="0.0.1",
    author="Bearer Team",
    author_email="engineering+python@bearer.sh",
    description="Bearer python helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bearer/python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Bearer python SDK"
    ],
)