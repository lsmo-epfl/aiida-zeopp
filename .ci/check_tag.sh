#!/bin/bash
# Checks that travis tag matches package version
VERSION=`python -c "from aiida_zeopp import __version__; print(__version__)"`
if [ "$TRAVIS_TAG" != "v$VERSION" ]; then
    echo "Travis tag $TRAVIS_TAG does not match package version $VERSION"
    exit 1 
fi
