from setuptools import setup

from grappler import version

setup(
    name=version.name,
    version=version.version,
    packages=[version.name],
    url=version.url,
    license=version.license,
    author=version.author,
    description=version.description
)
