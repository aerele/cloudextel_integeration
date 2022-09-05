from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in cloudextel_integeration/__init__.py
from cloudextel_integeration import __version__ as version

setup(
	name="cloudextel_integeration",
	version=version,
	description="App to integerate ERP with WMS",
	author="CloudExtel",
	author_email="hello@aerele.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
