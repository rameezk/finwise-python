{
  description = "Unofficial Python SDK for the FinWise API";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        pythonVersions = {
          python311 = pkgs.python311;
          python312 = pkgs.python312;
          python313 = pkgs.python313;
        };

        defaultPython = pythonVersions.python311;

        mkFinwise = python: python.pkgs.buildPythonPackage rec {
          pname = "finwise-python";
          version = "1.2.0";
          pyproject = true;

          src = pkgs.lib.cleanSourceWith {
            filter = name: type:
              let baseName = baseNameOf (toString name);
              in !(
                baseName == ".git" ||
                baseName == ".github" ||
                baseName == ".venv" ||
                baseName == ".mypy_cache" ||
                baseName == ".pytest_cache" ||
                baseName == ".ruff_cache" ||
                baseName == "site" ||
                baseName == "__pycache__" ||
                baseName == "result" ||
                baseName == ".direnv" ||
                pkgs.lib.hasSuffix ".egg-info" baseName
              );
            src = ./.;
          };

          build-system = with python.pkgs; [
            hatchling
          ];

          dependencies = with python.pkgs; [
            httpx
            pydantic
          ];

          nativeCheckInputs = with python.pkgs; [
            pytestCheckHook
            pytest-cov
            respx
          ];

          pythonImportsCheck = [ "finwise" ];

          meta = with pkgs.lib; {
            description = "Unofficial Python SDK for the FinWise API";
            homepage = "https://github.com/rameezk/finwise-python";
            license = licenses.mit;
            maintainers = [ ];
            platforms = platforms.unix;
          };
        };

        mkDevShell = python: pkgs.mkShell {
          packages = [
            (python.withPackages (ps: with ps; [
              httpx
              pydantic
              pytest
              pytest-cov
              respx
              mypy
              ruff
              hatchling
              pip
              build
            ]))
          ];

          shellHook = ''
            echo "FinWise Python SDK development environment"
            echo "Python version: $(python --version)"
          '';
        };

        docsShell = pkgs.mkShell {
          packages = [
            (defaultPython.withPackages (ps: with ps; [
              mkdocs
              mkdocs-material
            ]))
          ];

          shellHook = ''
            echo "FinWise Python SDK documentation environment"
            echo "Run 'mkdocs serve' to preview docs locally"
          '';
        };

      in {
        packages = {
          default = mkFinwise defaultPython;
          finwise-python311 = mkFinwise pythonVersions.python311;
          finwise-python312 = mkFinwise pythonVersions.python312;
          finwise-python313 = mkFinwise pythonVersions.python313;
        };

        devShells = {
          default = mkDevShell defaultPython;
          python311 = mkDevShell pythonVersions.python311;
          python312 = mkDevShell pythonVersions.python312;
          python313 = mkDevShell pythonVersions.python313;
          docs = docsShell;
        };

        apps = {
          docs-serve = {
            type = "app";
            program = toString (pkgs.writeShellScript "docs-serve" ''
              cd ${./.}
              ${defaultPython.withPackages (ps: with ps; [ mkdocs mkdocs-material ])}/bin/mkdocs serve
            '');
          };
          docs-build = {
            type = "app";
            program = toString (pkgs.writeShellScript "docs-build" ''
              cd ${./.}
              ${defaultPython.withPackages (ps: with ps; [ mkdocs mkdocs-material ])}/bin/mkdocs build
            '');
          };
        };

        checks = {
          default = mkFinwise defaultPython;
        };
      }
    );
}
