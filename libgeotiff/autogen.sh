#!/bin/sh
# $Id: autogen.sh 61 2007-12-11 20:13:48Z hobu $
#
# Autotools boostrapping script
#
# We deliberately limit this to automake and autoconf since
# we don't want geo_config.h.in regenerated automatically. 
#
echo "Running automake"
automake $AMFLAGS # || giveup
echo "Running autoconf"
autoconf || giveup

echo "======================================"
echo "Now you are ready to run './configure'"
echo "======================================"
