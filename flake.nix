{
  description = "A GitHub Pages development environment";

  inputs.nixpkgs-unstable.url = "nixpkgs/nixpkgs-unstable";

  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = {self, nixpkgs-unstable, flake-utils}:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = import nixpkgs-unstable { inherit system; }; in
      {
        devShell = pkgs.mkShell {
            buildInputs = [
              pkgs.html-proofer
              pkgs.rubyPackages.github-pages
            ];
        };
      }
    );
}
