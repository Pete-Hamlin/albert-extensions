#! /bin/bash
# Lazy install script - run from within this repository

if [ "$EUID" -ne 0 ]
    then echo Installing as user...
    DIR=$HOME/.local/share/albert/org.albert.extension.python/modules/
else
    echo Installing as root...
    DIR=/usr/share/albert/org.albert.extension.python/modules
fi
echo Installing extensions into $DIR
cp -r **/src/* $DIR
echo Done!