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

## .barbrc.toml
A configuration file is automatically created when the command `barb init` is run. The following are valid configurations
- `os-lock`
  - If enabled, git hooks will only attempt to execute on the specified operating system. Otherwise, they will be skipped.
  - ex. `os-lock = windows`
- `[os.$OS$.$FILE_EXT$]`
  - `interpreter`
    - The name (or path) of the interpreter to use for the file extension.
  - `args`
    - A list of arguments for the interpreter.
    - Note: the arguments are placed before the git hook path.
  - ```shell
    # Special Case: default interpreter for file ext with no interpreter specified
    [os.linux.default] 
    interpreter = 'bash'
  - ```shell
    # executes ps1 files as "powershell -ExecutionPolicy Unrestricted -File ./.barb/git-hook-name.ps1"
    [os.windows.ps1]
    interpreter = 'powershell'
    args = ['-ExecutionPolicy', 'Unrestricted', '-File']

### TODO:
- line endings, `barb sanitize` to sanitize the hooks?