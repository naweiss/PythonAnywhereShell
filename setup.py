from setuptools import setup, find_packages


setup(
    name='pythonanywhere-terminal',
    version='1.0.0',
    description='Python module and command line tool to connect to remote pythonanywhere consoles',

    author='Nadav Weiss',

    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'requests',
        'beautifulsoup4',
        'websockets>=8.0',
        'configargparse',
    ],

    entry_points = {
        'console_scripts': [
            'pyanywhere=pythonanywhere_terminal.anywhere:main'
        ],
    }
)
