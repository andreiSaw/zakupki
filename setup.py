try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name="zakupkiClient",
      version='1.0.1',
      description='zakupki client',
      url="https://github.com/andreisaw/zakupki",
      long_description=open('README.md').read(),
      author='Andrey',
      packages=["zakupkiClient"],
      install_requires=requirements
      )
