from setuptools import setup, find_packages

ld = 'Hassle free git hooks for python projects.'

setup(
    name='py-hook',
    version='0.0.1',
    author='Jett Crowson',
    author_email='jettcrowson@gmail.com',
    url='https://github.com/jettdc/py-hook',
    long_description=ld,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'py-hook = src.cli:main'
        ]
    },
    keywords='hooks git githooks automation'
)
