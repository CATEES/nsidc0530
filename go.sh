#!/bin/sh -e

conda update conda-build
conda build .
linuxpkg=$(conda build . --output)
anaconda upload --force -u catees $linuxpkg
for arch in osx-64; do
  conda convert -p $arch $linuxpkg
  archpkg=$arch/$(basename $linuxpkg)
  anaconda upload --force -u catees $archpkg
  rm -rf ./$arch
done
