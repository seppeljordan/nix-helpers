from distutils.core import setup

setup(
    name='nix-helpers',
    version='1.0',
    description='Utilities for working with Nix package manager',
    author='Sebastian Jordan',
    author_email='sebastian.jordan.mail@googlemail.com',
    url='https://github.com/seppeljordan/nix-helpers',
    packages=['nix.prefetch'],
    package_dir={'': 'src'},
)
