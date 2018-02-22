import os
import tempfile

import pytest
import nix.prefetch


def this_repo():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    abs_dirpath = os.path.abspath(dir_path)
    return os.path.split(os.path.split(abs_dirpath)[0])[0]


def in_nix_builder():
    env = os.environ
    print(env['HOME'])
    return all([
        env.get('PWD','').startswith('/tmp/nix-build'),
        env.get('HOME','').startswith('/homeless-shelter'),
    ])


skip_in_nix_builder = pytest.mark.skipif(
    in_nix_builder(),
    reason="cannot fetch stuff inside nix builder"
)


def test_prefetch_git_from_non_url_throws():
    with pytest.raises(Exception):
        svm.nix.prefetch_git('')


@skip_in_nix_builder
def test_checkout_repo_works_with_reference():
    with tempfile.TemporaryDirectory() as tempdir:
        nix.prefetch.checkout_repo(this_repo(), tempdir, local_mirror=this_repo())


@skip_in_nix_builder
def test_prefetch_git_this_repository_works_does_not_throw():
    prefetch_results = nix.prefetch.prefetch_git(this_repo())
    assert 'url' in prefetch_results.keys()


@skip_in_nix_builder
def test_prefetch_git_branch_returns_the_same_as_prefetch_git():
    assert (
        nix.prefetch.prefetch_git(this_repo())['sha256'] ==
        nix.prefetch.prefetch_git_branch(this_repo(), 'master')['sha256']
    )


@skip_in_nix_builder
def test_prefetch_github_works():
    nix.prefetch.prefetch_github("seppeljordan", "nix-helpers")
