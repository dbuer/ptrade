from setuptools import setup

setup(name="ptrade",
      version="0.0.1",
      description="python wrapper for the Etrade API",
      url="https://github.com/dbuer/ptrade",
      author="dbuer",
      packages=["ptrade"],
      python_requires=">=3.6",
      install_requires=[
          "requests_oauthlib>=1.3",
          "xmltodict>=0.12.0"
      ])