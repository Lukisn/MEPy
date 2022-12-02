#!/bin/zsh
python -m coverage run -m unittest
python -m coverage report
python -m coverage html

#open htmlcov/index.html
