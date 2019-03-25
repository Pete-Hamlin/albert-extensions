#! /bin/bash
# Run from within this folder
if [ "$EUID" -ne 0 ]
    then echo Installing as user...
    DIR=$HOME/.local/share/albert/org.albert.extension.python/modules/
else
    echo Installing as root...
    DIR=/usr/share/albert/org.albert.extension.python/modules
fi
echo Installing Pocket extension into $DIR
cp -r ./src/* $DIR
echo Done!