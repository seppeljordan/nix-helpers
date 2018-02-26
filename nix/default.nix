{ buildPythonPackage
, pytest
, mypy
, flake8
, nix-prefetch-scripts
, jinja2
, requests
, click
}:
buildPythonPackage {
  name = "svm-nix-helpers";
  src = ../.;
  propagatedBuildInputs = [
    click
    jinja2
    requests
  ];
  buildInputs = [
    pytest
    mypy
    flake8
    nix-prefetch-scripts
  ];
  checkPhase = ''
    echo $HOME
    make check
  '';
}
