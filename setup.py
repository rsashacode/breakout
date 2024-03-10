# pylint: disable=C0114
from setuptools import setup, find_packages

required = [
    'matplotlib==3.8.3',
    'pygame==2.5.2',
    'pydantic==2.6.3',
    'pytest==8.0.2',
]

setup(
    name='breakout_game',
    version='1.0.0',
    author='Aleksandr Rykov, Liu Chen-Yu',
    author_email='your.email@example.com',
    description='A modern version of the classic Breakout game made with PyGame',
    packages=find_packages(),
    install_requires=required,
    package_data={
        'breakout_game': [
            'assets/fonts/*',
            'assets/images/background/*', 'assets/images/ball/*', 'assets/images/blocks/*', 'assets/images/hearts/*',
            'assets/images/powerups/*',
            'assets/sounds/*'
        ]
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'breakout=breakout_game',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
