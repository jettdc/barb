# py-hook
Hassle free git hooks for python projects.

- `pip install py-hook`
- `py-hook init`
- look how husky does it, but initial thought is to just create all the hooks at the beginning and make them point to package functions that each time look to see if a user defined hook is available, otherwise do nothing.
- creates a .py-hook dir
- files within the dir are interpreted as hooks based on names
