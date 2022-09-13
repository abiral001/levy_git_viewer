from setuptools import setup

setup(
    name='levy-gitlogger',
    version='0.1.3',
    description='local git commits to csv file logger',
    url='https://github.com/abiral001/levy_git_viewer',
    author="abiralp",
    author_email="",
    license="MIT",
    packages=['levy'],
    install_requires=['pandas',
                      'gitpython',
                      ],
    entry_points={
        'console_scripts': [
            'levy=levy.main:main'
        ]
    }
)