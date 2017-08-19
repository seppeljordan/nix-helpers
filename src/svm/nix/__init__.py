import subprocess
import json


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
