#!/bin/bash

# Be verbose, and stop with error as soon there's one
set -ev

python -m unittest discover
