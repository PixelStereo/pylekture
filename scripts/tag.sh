#!/bin/sh

# One day, this script will write the current tag into setup.py before deploying to pypi

set -v

echo "TAG" $TRAVIS_TAG
echo "COMMIT" $TRAVIS_COMMIT
