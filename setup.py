import pathlib

from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
exec(open(HERE / "shift4/__version__.py").read())
INSTALL_REQUIRES = (HERE / "requirements.txt").read_text().splitlines()


setup(
    name="shift4",
    version=__version__,
    description="Shift4 Python Library",
    long_description="Python library for Shift4 API",
    url="https://github.com/shift4developer/shift4-python",
    author="Shift4",
    author_email="devsupport@shift4.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="payment",
    packages=find_packages(exclude=["tests*"]),
    install_requires=INSTALL_REQUIRES,
    test_suite="tests",
)
