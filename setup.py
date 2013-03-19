from distutils.core import setup
from setuptools import find_packages

setup(name="django-sorl-cropping",
    version="0.1.0",
    description="A reusable app for cropping images easily and non-destructively in Django",
    long_description=open('README.rst').read(),
    author="Ilya Chistyakov",
    author_email="ilchistyakov@gmail.com",
    url="http://github.com/NElias/django-sorl-cropping",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=1.4.5',
        'sorl-thumbnail>=11.12',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
