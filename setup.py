from setuptools import setup

setup(
   name='contacts-api',
   version='1.0',
   description='A simple contacts api written in python',
   author='Ben White',
   author_email='benjiman.white@gmail.com',
   packages=['contacts_api'],  #same as name
   install_requires=['flask', 'pytest'], #external packages as dependencies
)
