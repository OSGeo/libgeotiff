#!/bin/sh

if [ $# -lt 1 ] ; then
  echo "Usage: mkdist.sh version [-install]"
  echo
  echo "Example: mkdist.sh 1.1.5"
  exit
fi

VERSION=$1
COMPRESSED_VERSION=`echo $VERSION | tr -d .`

rm -rf dist_wrk  
mkdir dist_wrk
cd dist_wrk

export CVSROOT=:pserver:anonymous@cvs.remotesensing.org:/cvsroot

echo "Please type anonymous if prompted for a password."
cvs login

cvs checkout geotiff/libgeotiff

if [ \! -d geotiff/libgeotiff ] ; then
  echo "cvs checkout reported an error ... abandoning mkdist.sh"
  exit
fi

find geotiff -name CVS -exec rm -rf {} \;

mv geotiff/libgeotiff libgeotiff-${VERSION}

rm -f ../libgeotiff-${VERSION}.tar.gz ../libgeotiff${COMPRESSED_VERSION}.zip

tar cf ../libgeotiff-${VERSION}.tar libgeotiff-${VERSION}
gzip -9 ../libgeotiff-${VERSION}.tar
zip -r ../libgeotiff${COMPRESSED_VERSION}.zip libgeotiff-${VERSION}


cd ..
rm -rf dist_wrk

TARGETDIR=/ftp/remotesensing/pub/geotiff/libgeotiff
if test "$2" = "-install" ; then
  if test \! -d $TARGETDIR ; then
    echo "Can't find $TARGETDIR ... -install failed."
    exit
  fi

  echo "Installing: " $TARGETDIR/libgeotiff-${VERSION}.tar.gz
  rm -f $TARGETDIR/libgeotiff-${VERSION}.tar.gz
  cp libgeotiff-${VERSION}.tar.gz $TARGETDIR

  echo "Installing: " $TARGETDIR/libgeotiff${COMPRESSED_VERSION}.zip
  rm -f $TARGETDIR/libgeotiff${COMPRESSED_VERSION}.zip
  cp libgeotiff${COMPRESSED_VERSION}.zip $TARGETDIR
fi
