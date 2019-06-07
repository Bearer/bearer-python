import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bearer",
    version="1.0.0",
    author="Bearer Team",
    author_email="engineering+python@bearer.sh",
    description="Bearer python helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bearer/bearer-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "requests[security]>=2.9.1"
    ],
    setup_requires=[
        "pytest-runner",
        "twine",
        "wheel"
    ],
    tests_require=[
        "faker",
        "pytest",
        "requests_mock"
    ]
)
