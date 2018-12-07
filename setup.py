from setuptools import setup, find_packages

setup(name='trellotools',
    version='0.0.0',
    description='Trello tools',
    url='https://github.com/Faheetah/trello-updater',
    author='Faheetah',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'trello=cli:main',
        ],
    },
    install_requires=[
        'requests>=2.19.0',
        'argparse>=1.4.0',
        'PyYAML>=3.13',
        'Flask>=1.0.2',
        'gevent>=1.3.7',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-watch',
            'pytest-testmon',
        ]
    }

)
