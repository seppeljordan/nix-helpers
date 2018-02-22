import json
import os
import re
import subprocess
from tempfile import TemporaryDirectory

import jinja2
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


def prefetch_github(owner, repo, rev=None):
    calculated_rev = get_latest_commit_from_github(owner, repo)
    actual_rev = rev or calculated_rev
    templates_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(HERE + '/templates'),
    )
    template = templates_env.get_template('prefetch-github.nix.j2')
    nix_prefetch_code = template.render(
        owner=owner,
        repo=repo,
        rev=actual_rev,
        fake_hash='1y4ly7lgqm03wap4mh01yzcmvryp29w739fy07zzvz15h2z9x3dv',
    )
    with TemporaryDirectory() as temp_dir_name:
        nix_filename = temp_dir_name + '/prefetch-github.nix'
        with open(nix_filename, 'w') as f:
            f.write(nix_prefetch_code)
        returncode, output = cmd(['nix-build', nix_filename])
    r = re.compile(
        "output path .* has .* hash (.*) when .*"
    )
    calculated_hash = None
    for line in output.splitlines():
        re_match = r.match(line)
        if re_match:
            calculated_hash = re_match.group(1)[1:-1]
            break
    if calculated_hash:
        return {
            "rev": actual_rev,
            "sha256": calculated_hash,
        }
    else:
        raise Exception(
            (
                'Internal Error: Calculate hash value for sources '
                'in github repo {owner}/{repo}.\n\noutput was: {output}'
            ).format(owner=owner, repo=repo, output=output)
        )
