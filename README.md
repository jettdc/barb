# barb
Hassle free git hooks for python projects

![PyPi Download](https://img.shields.io/pypi/v/barb)
![PyPi Download](https://img.shields.io/pypi/l/barb)
![PyPi Download](https://img.shields.io/pypi/pyversions/barb)

## Installation
`pip install barb`

## Initializing a new project
`barb init`

Running this command both initializes the `.barb` directory as well as runs the `barb install` command.

## Installing barb
To register the hooks under the `.barb` directory with git, run `barb install`

## Creating a hook
Create a script under the `.barb` directory with the same name as the git hook you are attempting to create.

You can create two types of scripts to work as hooks:
- The standard shell script, which will be executed by bash.  
ex.
```shell
./.barb/pre-commit
---
#!/bin/sh
echo "Hello, World!"
```
- A python script. The script will enter at the `hook()` function
```shell
./.barb/pre-push.py
---
def hook():
  print('Hello, World!')
```
_Exceptions and False return values from this function will be considered hook failures._
