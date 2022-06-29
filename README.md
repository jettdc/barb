# barb
Hassle-free, cross-platform git hooks for python projects

![PyPi Download](https://img.shields.io/pypi/v/barb)
![PyPi Download](https://img.shields.io/pypi/l/barb)

[//]: # (![PyPi Download]&#40;https://img.shields.io/pypi/pyversions/barb&#41;)

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
- The standard shell script, which will be executed by the operating system's default cli.  
ex.
```shell
./.barb/pre-commit
---
#!/bin/sh
echo "Hello, World!"
```
- A python script. The script will enter at the `hook()` function. Not all hooks pass arguments, but those that provide
them do so via the args parameter.
```shell
./.barb/pre-push.py
---
def hook(*args):
  print('Hello, World!')
```
_Exceptions and False return values from this function will be considered hook failures._

Hooks can be organized in one of two ways. Top level files will be run on each os, without consideration:
```
.barb
├── pre-commit
└── post-rewrite.py
```

Alternatively, when organized in folders, different scripts can be set to run depending on the operating system:
```
.barb
└── post-rewrite
    ├── linux.py
    ├── darwin
    └── windows.ps1
```

### TODO:
- line endings, `barb sanitize` to sanitize the hooks?