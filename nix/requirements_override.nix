{ pkgs, python }:

self: super: {
  pytest = super.pytest.overrideDerivation( old: {
      patchPhase = ''
        sed -i "s|setup_requires=\['setuptools-scm'\],||" setup.py
      '';
    });
}
