# barb 🪝
Hassle free git hooks for python projects

## Installation
`pip install barb`

## Initializing a new project
`barb init`

Running this command both initializes the `.barb` directory as well as runs the `barb install` command.

## Installing barb
To register the hooks under the `.barb` directory with git, run `barb install`

## Creating a hook
Create a script under the `.barb` directory with the same name as the git hook you are attempting to create.

ex.
```shell
#!/bin/sh
echo "Hello, World!"
```
