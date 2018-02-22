{ pkgs, python }:

let
  notPytest = drv:
    ! (pkgs.lib.hasSuffix "-pytest"
     (builtins.parseDrvName drv.name).name);
in

self: super: {
  attrs = super.attrs.overrideDerivation (old: {
      propagatedBuildInputs = with builtins;
        filter notPytest old.propagatedBuildInputs;
  });
}
