# Installation

## Requirements

- Python 3.11 or higher

## From PyPI

Install the SDK using pip:

```bash
pip install finwise-python
```

## Using Nix

If you have [Nix](https://nixos.org/) installed with flakes enabled, you can use this package directly:

```bash
# Build the package
nix build github:rameezk/finwise-python

# Or use in your flake.nix
{
  inputs.finwise-python.url = "github:rameezk/finwise-python";
}
```

## For Development

If you want to contribute or modify the SDK:

```bash
pip install finwise-python[dev]
```

Or with Nix:

```bash
git clone https://github.com/rameezk/finwise-python.git
cd finwise-python
nix develop
pip install -e .
```

## For Documentation

To build the documentation locally:

```bash
pip install finwise-python[docs]
```

Or with Nix:

```bash
nix develop .#docs
mkdocs serve
```
