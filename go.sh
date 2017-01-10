#!/bin/sh -e

conda update conda-build
conda build .
linuxpkg=$(conda build . --output)
anaconda upload --force -u catees $linuxpkg
conda convert -p osx-64 $linuxpkg
osxpkg=osx-64/$(basename $linuxpkg)
anaconda upload --force -u catees $osxpkg
rm -rf ./osx-64
