# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Causal Inference
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='causal_inference',
      version='0.0.1',
      description='Causal Inference',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/ga74kud/causal_inference',
      author='Michael Hartmann',
      author_email='michael.hartmann@v2c2.at',
      license='GNU GENERAL PUBLIC LICENSE',
      packages=setuptools.find_packages(),
      install_requires=[
          "scipy",
          "numpy",
          "matplotlib",
          "argparse",
          "python-igraph",
          "pycairo",
          "plotly",
          "pandas",
        ],
      zip_safe=False)
