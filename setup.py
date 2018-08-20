# coding: utf-8
from setuptools import setup, find_packages
from pip.req import parse_requirements

install_requires = [str(ir.req) for ir in parse_requirements("requirements.txt", session=False)]


setup(
    name='seswatcher',
    version='0.2',
    author='KhanhIceTea',
    author_email="khanhicetea@gmail.com",
    url="https://github.com/khanhicetea/seswatcher",
    py_modules=['seswatcher'],
    packages=find_packages(),
    description='A small tool to prevent AWS SES from blocked by exceeding Bounces Rate or Complaints Rate',
    dependency_links=[],
    keywords=['ses', 'aws'],
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        seswatcher=seswatcher.main:watch
    ''',
)