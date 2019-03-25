#! /bin/bash
# Lazy install script - run from within this repository

if [ "$EUID" -ne 0 ]
    then echo Running as user...
    DIR=$HOME/.local/share/albert/org.albert.extension.python/modules/
else
    echo Running as root...
    DIR=/usr/share/albert/org.albert.extension.python/modules
fi
echo Installing extensions
**/install.sh
echo Done!