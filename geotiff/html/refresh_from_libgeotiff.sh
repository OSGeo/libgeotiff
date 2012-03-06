#!/bin/sh

LIBGEOTIFF_DIR=../../libgeotiff

if [ "$1" != "" ] ; then
  LIBGEOTIFF_DIR=$1
fi

if [ ! -d $LIBGEOTIFF_DIR -o ! -f $LIBGEOTIFF_DIR/docs/Doxyfile ] ; then
  echo "Did not find libgeotiff directory at $LIBGEOTIFF"
  echo "The location of the checked out libgeotiff directory can be provided"
  echo "as the argument to this script."
  exit 1;
fi

(cd $LIBGEOTIFF_DIR ; make docs)

cp $LIBGEOTIFF_DIR/docs/api/* api
cp $LIBGEOTIFF_DIR/docs/*.html . 





