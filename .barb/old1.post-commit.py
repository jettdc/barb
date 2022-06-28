import sys


def hook(*args):
    print(f"Finished up the commit: {str(args)}")
