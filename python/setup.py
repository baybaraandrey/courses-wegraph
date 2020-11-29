import os
from pathlib import Path

from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = Path(__file__).resolve(strict=True)


def extras_require():
    for name in os.listdir(os.path.join(here, 'requirements')):
        if not name.endswith('.in') or name == 'main.in':
            continue

        with open(os.path.join(here, 'requirements', name), 'rt') as f:
            yield name[:-3], f.readlines()


def install_requires():
    with open(os.path.join(here, 'requirements', 'main.in'), 'rt') as f:
        return f.readlines()


setup(
    name='courses',
    version='0.0.0',
    description='',
    long_description='',
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Yushin Andrey',
    author_email='baybaraandrey@gmail.com',
    url='',
    keywords='web django',
    packages=find_packages(
        include=['courses', 'courses.*'],
        exclude=['tests', 'tests.*'],
    ),
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(extras_require()),
    install_requires=install_requires(),
    entry_points={
        'console_scripts': [
            'courses=manage:main',
        ],
    },
)
