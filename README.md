# debug_printer

A very simple Python module that allows for printing text to a file with ANSI color strings.

The intent is to be able to `tail` a file in order to provide an additional source of information. For those times when you need information without clogging up your generic output and dropping into a debug session is unnecessary.

I am intentionally **not** using the native logging system. This is intended as a simple drop-in module with very basic support for my own coding workflow.

## Note
It is generally preferable to drop into a PDB shell for debugging. This is **not** meant to replace that. Please don't allow printing everything to become a habit. The road to hell is paved with `print()` statements.

## Installation
Please, **please** do not install to your system site packages. The road to hell is also paved with `sudo pip install`

Even installing under `uid 0` in a container is a seriously bad idea. 

1) `cd` into a temporary directory
2) `git clone https://github.io/koepnick/debug_printer`
3) If using a virtual environment: `python setup.py install`
-- or --
3) If using "globally": `python setup.py install --user`

## Features
- [x] Basic coloring
- [x] Stateless singleton
- [x] Symbolic icons
- [ ] UTF-8 icon fallback
- [ ] User-defined colors
- [ ] Settings file
- [ ] Vim functions to write and populate line numbers
- [ ] Object ancestry
- [ ] List enumeration
* [ ] PyPi submission
