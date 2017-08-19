let
  nixpkgs = import <nixpkgs> {};
  python = import nix/requirements.nix { pkgs = nixpkgs; };
in
  with nixpkgs;
  stdenv.mkDerivation {
    name = "development-env";
    buildInputs = [ python.interpreter ];
  }
