from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='barb',
    version='0.0.8',
    author='Jett Crowson',
    author_email='jettcrowson@gmail.com',
    url='https://github.com/jettdc/barb',
    description='Hassle free git hooks for python projects.',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'barb = src.cli:main'
        ]
    },
    keywords='hooks git githooks automation',
    python_requires='>=3.5'
)
