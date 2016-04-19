#!/bin/bash
set -ev

if [ "${TRAVIS_PYTHON_VERSION}" != 2.7 ]; then
	coverage xml
	coverage report -m
	python-codacy-coverage -r coverage.xml

fi
