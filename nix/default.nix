{ buildPythonPackage
, pytest
, mypy
, flake8
, nix-prefetch-scripts
, jinja2
, requests
}:
buildPythonPackage {
  name = "svm-nix-helpers";
  src = ../.;
  buildInputs = [
    pytest
    mypy
    flake8
    nix-prefetch-scripts
    requests
    jinja2
  ];
  checkPhase = ''
    echo $HOME
    make check
  '';
}
