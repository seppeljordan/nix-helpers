import os

import pytest
import svm.nix


def this_repo():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    abs_dirpath = os.path.abspath(dir_path)
    return os.path.split(os.path.split(abs_dirpath)[0])[0]


def in_nix_builder():
    return os.environ.get('NIX_BUILD_TOP')


def test_prefetch_git_from_non_url_throws():
    with pytest.raises(Exception):
        svm.nix.prefetch_git('')


def test_prefetch_git_this_repository_works_does_not_throw():
    if in_nix_builder():
        pytest.skip("inside of nix builder")
    else:
        prefetch_results = svm.nix.prefetch_git(this_repo())
        assert 'url' in prefetch_results.keys()
