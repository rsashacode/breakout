from setuptools import setup, find_packages

required = [
    'matplotlib==3.8.3',
    'pygame==2.5.2',
    'pydantic==2.6.3',
    'pytest==8.0.2',
]

setup(
    name='BreakoutGame',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A modern version of the classic Breakout game made with PyGame',
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'breakout=breakout_module:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
