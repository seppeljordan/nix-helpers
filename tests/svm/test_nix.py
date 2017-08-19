import svm.nix
import pytest


def test_prefetch_git_from_non_url_throws():
    with pytest.raises(Exception):
        svm.nix.prefetch_git('')
