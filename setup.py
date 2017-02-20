from setuptools import setup
from setuptools import find_packages


setup(name='googleImageDownloader',
      version='0.1',
      description='Helper for Flickr photos.search API',
      author='Riccardo Del Chiaro',
      author_email='riccardo.delchiaro@gmail.com',
      url='https://github.com/nagash91/python-google-image-downloader',
      license='MIT',
      packages=find_packages(),
      package_dir={'googleImageDownloader': 'googleImageDownloader'},
      long_description=open('README.md').read(),
      requires=['requests']
      )
