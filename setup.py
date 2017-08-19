from distutils.core import setup

setup(
    name='svm-nix-helpers',
    version='1.0',
    description='Utilities for working with Nix package manager',
    author='Sebastian Jordan',
    author_email='jordan@schneevonmorgen.com',
    url='https://github.com/schneevonmorgen/nix-helpers',
    packages=['svm.nix'],
    package_dir={'': 'src'},
)
