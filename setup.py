from setuptools import setup, find_packages
from src.version import VERSION

with open('README.md') as f:
    readme = f.read()

setup(
    name='barb',
    version=VERSION,
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
    keywords='hooks git githooks automation git-hooks git-hook',
    python_requires='>=3.5',
    install_requires=['toml', 'python-dotenv', 'jetts-tools']
)
