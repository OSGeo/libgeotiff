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

export CVSROOT=:pserver:cvsanon@cvs.maptools.org:/cvs/maptools/cvsroot

echo "Please type anonymous if prompted for a password."
cvs login

cvs checkout geotiff/libgeotiff

if [ \! -d geotiff/libgeotiff ] ; then
  echo "cvs checkout reported an error ... abandoning mkdist.sh"
  exit
fi

find geotiff -name CVS -exec rm -rf {} \;

mv geotiff/libgeotiff libgeotiff-${VERSION}
touch libgeotiff-${VERSION}/configure

rm -f ../libgeotiff-${VERSION}.tar.gz ../libgeotiff${COMPRESSED_VERSION}.zip

tar cf ../libgeotiff-${VERSION}.tar libgeotiff-${VERSION}
gzip -9 ../libgeotiff-${VERSION}.tar
zip -r ../libgeotiff${COMPRESSED_VERSION}.zip libgeotiff-${VERSION}


cd ..
rm -rf dist_wrk

TARGETDIR=remotesensing.org:/ftp/remotesensing/pub/geotiff/libgeotiff
if test "$2" = "-install" ; then
  scp libgeotiff-${VERSION}.tar.gz libgeotiff${COMPRESSED_VERSION}.zip \
	$TARGETDIR
fi
