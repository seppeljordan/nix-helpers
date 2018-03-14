import json
import os
import subprocess
from tempfile import TemporaryDirectory

import requests

HERE = os.path.dirname(__file__)


def cmd(command):
    process_return = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    return process_return.returncode, process_return.stdout


def prefetch_git(url, revision=None):
    cmd = [
        'nix-prefetch-git',
        url
    ] + (['--rev', revision] if revision else [])

    process_return = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    if process_return.returncode == 0:
        prefetch_result = json.loads(process_return.stdout)
        return {
            'url': prefetch_result['url'],
            'rev': prefetch_result['rev'],
            'sha256': prefetch_result['sha256'],
        }
    elif process_return.returncode == 127:
        raise Exception('nix-prefetch-git is not in path')
    else:
        raise Exception(
            ' '.join(
                ['An unexpected error occured while executing',
                 '`nix-prefetch-git`.  stdout was: `{stdout}`, stderr was:',
                 '`{stderr}`']
            ).format(
                stdout=process_return.stdout,
                stderr=process_return.stderr,
            )
        )


def checkout_repo(
        url, working_directory, local_mirror=None
):
    cmd = [
        'git',
        'clone',
        url,
        working_directory
    ] + (
        ['--reference', local_mirror] if
        local_mirror is not None
        else []
    )
    subprocess.run(cmd)


def checkout_branch(branch_name, workdir):
    cmd = [
        'git',
        'checkout',
        branch_name
    ]
    subprocess.run(cmd, cwd=workdir)


def prefetch_git_branch(
        url, branch, local_mirror=None
):
    with TemporaryDirectory() as tempdir:
        checkout_repo(url, tempdir, local_mirror)
        checkout_branch(branch, tempdir)
        prefetch_data = prefetch_git(os.path.abspath(tempdir))
        prefetch_data['url'] = url
        return prefetch_data


def get_latest_commit_from_github(owner, repo):
    url_template = 'https://api.github.com/repos/{owner}/{repo}/commits/master'
    request_url = url_template.format(
        owner=owner,
        repo=repo,
    )
    response = requests.get(request_url)
    return response.json()['sha']
