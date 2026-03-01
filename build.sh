#!/bin/bash

python3 scripts/check_notebook_kernelspec.py
jupyter-book clean --html .
jupyter-book build .
