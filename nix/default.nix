{ buildPythonPackage, pytest, mypy, flake8, nix-prefetch-scripts }:
buildPythonPackage {
  name = "svm-nix-helpers";
  src = ../.;
  buildInputs = [ pytest mypy flake8 nix-prefetch-scripts ];
  checkPhase = ''
    echo $HOME
    make check
  '';
}
