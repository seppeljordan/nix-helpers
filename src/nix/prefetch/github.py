import json

import click
from nix.prefetch import prefetch_github


@click.command('nix-prefetch-github')
@click.argument('owner')
@click.argument('repo')
def main(owner, repo):
    repo_data = prefetch_github(owner, repo)
    print(
        json.dumps(
            {
                "owner": owner,
                "repo": repo,
                "rev": repo_data['rev'],
                "sha256": repo_data['sha256'],
            },
            indent=4,
        )
    )


if __name__ == "__main__":
    main()
