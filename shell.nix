with import <nixpkgs> {};

let
  python-with-packages = python3.withPackages (ps: with ps; [
    psutil
    colorama
    art
  ]);
in
pkgs.mkShell {
  buildInputs = [
    python-with-packages
    (python3.pkgs.buildPythonPackage rec {
      pname = "pwinput";
      version = "1.0.3";
      src = python3.pkgs.fetchPypi {
        inherit pname version;
        sha256 = "yhqL0G4ohy11Hb1BMthjcSfCW0COo6NJN3MUpUkUJvM=";
      };
      doCheck = false;
    })
  ];
}
