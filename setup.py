# setup.py at project root
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [r.strip() for r in f if r.strip() and not r.startswith("#")]

setup(
    name="research-assistant",
    version="0.1.0",
    author="Taufeeq Ahmad",
    packages=find_packages(exclude=["tests", "*.tests", "backend.tests", "frontend.*.tests"]),
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "research-backend=backend.app.main:main",
        ],
    },
)
