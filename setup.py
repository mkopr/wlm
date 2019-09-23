from setuptools import find_packages, setup

setup(
    python_requires=">=3.7",
    name='website_measure',
    version='1.0.0',
    author='Marcin Koprek',
    author_email='marcinkoprek@gmail.com',
    packages=find_packages(include=('website_measure*',)),
    install_requires=open('requirements.txt').read(),
    entry_points={
        'console_scripts': [
            'wlm = website_measure:run',
        ],
    },
)
