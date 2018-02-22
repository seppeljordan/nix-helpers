with (import <nixpkgs> {});
python3Packages.callPackage nix/default.nix {
  jinja2 = python3Packages.jinja2;
  requests = python3Packages.requests;
}
