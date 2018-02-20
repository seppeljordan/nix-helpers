import json
import os
import subprocess
import tempfile


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
    with tempfile.TemporaryDirectory() as tempdir:
        checkout_repo(url, tempdir, local_mirror)
        checkout_branch(branch, tempdir)
        prefetch_data = prefetch_git(os.path.abspath(tempdir))
        prefetch_data['url'] = url
        return prefetch_data
