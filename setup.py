from setuptools import find_packages, setup

setup(
    name='expander',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'expander = expander.cli:main'
        ]
    }
)
